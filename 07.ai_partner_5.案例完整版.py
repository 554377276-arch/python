import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json



st.set_page_config(
    page_title="ai 智能伴侣",
    page_icon="🧊",
    #布局
    layout="wide",
    #侧边栏
    initial_sidebar_state="expanded",
    menu_items={}
)
#生成会话标识的函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


#保存会话数据的函数
def save_session():
    if st.session_state.curent_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "messages": st.session_state.messages,
            "curent_session": st.session_state.curent_session
        }
        # 如果 sessions 目录不存在则创建
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        # 保存文件数据
        with open(f"sessions/{st.session_state.curent_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
#加载所有的会话列表函数
def load_sessions():
    sessions_list = []
    #加载sessions目录下的所有文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                sessions_list.append(filename[:-5])
    sessions_list.sort(reverse=True)#排序
    return sessions_list
#加载指定信息函数
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话失败: {e}")
#删除会话函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")#删除文件
            #如果删除的是当前会话则需要跟新当前会话
            if session_name == st.session_state.curent_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()

    except Exception as e:
        st.error(f"删除会话失败: {e}")
#大标题
st.title("ai 智能伴侣")
#logo
st.logo("资源/321.png")
#系统提示词
system_prompt = """
        你叫%s,现在是用户的真实伴侣,请完全代入角色
        规则:
            1.每次回复1条消息
            2.禁止描述场景
            3.匹配用户语言
            4.回复简短,像微信聊天一样
            5.有需要的话可以用表情符号
            6.用符合伴侣性格的方式说话
            7.回复内容要充分体现伴侣性格特征
        伴侣性格
            %s
        你必须严格遵守以上规则回复用户
    """
#初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []
#昵称
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "yy"
#性格
if 'nature' not in st.session_state:
    st.session_state.nature = "开朗的浙江姑娘"
#会话标识
if 'curent_session'  not in st.session_state:
    st.session_state.curent_session = generate_session_name()
#展示聊天信息
st.text(f"会话名称:{st.session_state.curent_session}")
for message in st.session_state.messages:#{"role": "user", "content": prompt},
    st.chat_message(message["role"]).write(message["content"])

#ai配置环境
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")






#左侧的侧边栏- with 是streamlit中的上下文管理器
with st.sidebar:
    #会话信息
    st.subheader("ai控制面板")
    #新建会话按钮
    if st.button("新建会话",width="stretch",icon="✏️"):
        #1.保存当前数据
        save_session()

        #2.新建会话
        if st.session_state.messages:#如果聊天记录非空,true;否则false
            st.session_state.messages = []
            st.session_state.curent_session = generate_session_name()
            save_session()
            st.rerun ()#重新运行当前页面
    #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        coll1,coll2 =  st.columns([4,1])
        with coll1:
            #加载会话信息
            #三元运输符:如果条件为真返回第一个值,否则返回第二个值--语法;值1 if 条件 else 值2
            if st.button(session,width="stretch",icon="📂",key=f"loda_{session}",type="primary"if session == st.session_state.curent_session else "secondary"):
                load_session(session)
                st.rerun()

        with coll2:
            #删除会话信息
            if st.button("",width="stretch",icon="🗑️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()
    #分割线
    st.divider()

    #伴侣信息
    st.subheader("伴侣信息")
    #昵称
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    #性格
    nature = st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature
#输入框
prompt = st.chat_input("请输入你的问题")
if prompt:#字符串会自动转化bool
    st.chat_message("user").write(prompt)
    print("调用ai llm 提示词", prompt)
    #保存用户输入提示词
    st.session_state.messages.append({"role": "user", "content": prompt})


    #调用ai
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name,st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True,
    )
    # 输出结果(非流式输出解析方式)
    # print("大模型返回结果", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # 输出结果(流式输出解析方式)
    response_message = st.empty()#创建一个空元素
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)


    #保存llm返回结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    #保存会话信息
    save_session()



















