import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import traceback

st.set_page_config(layout="wide")
st.title("Leafmap - Vector + Raster (Sentinel-2 Test)")

# --- 【替換 COG 來源】 ---
# 使用 AWS Open Data 上的 Sentinel-2 COG 影像 (一個特定區域)
cog_url = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/34/S/DJ/2020/7/S2B_34SDJ_20200701_0_L2A/TCI.tif"

# 向量資料 URL (保持不變)
vector_url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

gdf = None
try:
    gdf = gpd.read_file(vector_url)
    # st.success("成功載入向量資料 (Countries GDF)。") # 暫時隱藏訊息
except Exception as e:
    st.error(f"載入向量資料時發生錯誤: {e}")
    st.code(traceback.format_exc())

# --- 建立地圖物件 ---
# 稍微調整中心點以符合 Sentinel-2 影像區域
m = leafmap.Map(center=[14.5, 38.5], zoom=8) # 調整中心和縮放

# --- 嘗試加入 Sentinel-2 COG 圖層 ---
try:
    st.info(f"嘗試從 AWS 加入 Sentinel-2 COG 圖層: {cog_url}")
    m.add_cog_layer(
        cog_url,
        endpoint="https://titiler.xyz/", # 保持使用 titiler.xyz
        indexes=[1, 2, 3],  # Sentinel-2 TCI 是 RGB 影像，使用 1, 2, 3 波段
        # rescale 不再需要，因為 RGB 影像通常是 0-255
        # palette 也不需要，因為是 RGB 真實色彩
        name="Sentinel-2 TCI (RGB)"
    )
    st.success("已嘗試加入 Sentinel-2 COG 圖層。請檢查地圖和圖層控制器。")

except Exception as e:
    st.error(f"加入 Sentinel-2 COG 圖層時發生錯誤: {e}")
    st.error("這可能是暫時的網路問題或 Titiler 服務不相容。")
    st.code(traceback.format_exc())

# --- 嘗試加入向量圖層 (如果 GDF 成功載入) ---
if gdf is not None:
    try:
        m.add_gdf(
            gdf,
            layer_name="Global Countries (Vector)",
            # zoom_to_layer=True, # 暫時關閉縮放到全球
            info_mode='on_click',
            style={"fillOpacity": 0, "color": "black", "weight": 0.5}
        )
        # st.success("已嘗試加入向量圖層。請檢查地圖和圖層控制器。") # 暫時隱藏訊息
    except Exception as e:
        st.error(f"加入向量圖層時發生錯誤: {e}")
        st.code(traceback.format_exc())

# --- 加入圖層控制器並顯示地圖 ---
try:
    m.add_layer_control()
    m.to_streamlit(height=700)
except Exception as e:
    st.error(f"顯示地圖或圖層控制器時發生錯誤: {e}")
    st.code(traceback.format_exc())