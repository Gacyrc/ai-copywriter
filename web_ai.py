import streamlit as st
import requests

# 网页配置
st.set_page_config(page_title="爆款文案工厂", page_icon="🏭", layout="centered")
st.title("🏭 爆款文案工厂 (v2.0)")
st.caption("自研 AI 引擎驱动，一键生成闲鱼/小红书高转化文案。")

# 你的 API Key (记得替换成真实的)
api_key = st.secrets["DEEPSEEK API_KEY"]

# 用两列排版输入框和下拉菜单
col1, col2 = st.columns([2, 1])

with col1:
    product = st.text_input("输入你要卖的商品名称：", placeholder="例如：99新 索尼微单相机")
with col2:
    # 风格选择下拉菜单
    style = st.selectbox("选择文案风格：", 
                         ["闲鱼搞笑风（情绪拉满）", 
                          "小红书种草风（绝绝子）", 
                          "专业数码风（硬核参数）"])

# 核心生成逻辑
if st.button("🚀 一键生成爆款文案", use_container_width=True):
    if not product:
        st.warning("老板，先输入个商品吧！")
    else:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 根据用户的选择，动态改变提示词
        system_prompt = f"你是一个爆款闲鱼文案大师。请用【{style}】的风格，帮我写个卖【{product}】的文案。要求多用emoji，排版清晰，直接输出结果，不要废话。"
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "开始写。"}
            ]
        }
        
        with st.spinner("AI 正在疯狂码字中，请稍候..."):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                st.success("文案生成完毕！请复制下方内容：")
                
                # 把生成的文案放在一个好看的框里
                st.info(answer)
            else:
                st.error(f"调用失败，错误代码：{response.status_code}。请检查 API Key。")