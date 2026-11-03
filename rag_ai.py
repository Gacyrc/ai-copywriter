import streamlit as st
import requests
import streamlit as st

# ================= 访问密码锁 =================
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔒 内部系统登录")
    pwd = st.text_input("请输入访问密码：", type="password")
    if st.button("登录"):
        if pwd == "888888":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("密码错误，请重试！")
    st.stop()  # 密码不对，后面的代码全部停止运行！
# ==============================================

st.set_page_config(page_title="AI 专属知识库", page_icon="📚")
st.title("📚 AI 专属文档问答助手")
st.caption("上传你的 TXT 文档，AI 将基于文档内容为你解答。")

# 你的 API Key
api_key = st.secrets["DEEPSEEK_API_KEY"]

# 1. 上传文件组件
uploaded_file = st.file_uploader("请上传一个 TXT 文本文件", type=["txt"])

if uploaded_file is not None:
    # 读取文件内容
    file_content = uploaded_file.read().decode("utf-8")
    st.success("文件上传成功！可以开始提问了。")
    
    # 2. 聊天输入框
    question = st.text_input("针对这份文档，你想问什么？")
    
    if st.button("开始提问"):
        if not question:
            st.warning("请输入问题！")
        else:
            # 3. 核心逻辑：把文档内容和问题一起发给 AI
            url = "https://api.deepseek.com/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # 🚨 这就是 RAG 的灵魂：构造带上下文的提示词
            system_prompt = f"""
            你是一个专业的文档分析助手。请只根据我提供的【参考文档】来回答问题。
            如果参考文档中没有答案，请直接回答“文档中未提及”，绝对不要自己瞎编。
            
            【参考文档】：
            {file_content}
            """
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            }
            
            with st.spinner("AI 正在阅读文档并思考..."):
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.info("💡 AI 的回答：")
                    st.write(answer)
                else:
                    st.error(f"调用失败，错误代码：{response.status_code}")