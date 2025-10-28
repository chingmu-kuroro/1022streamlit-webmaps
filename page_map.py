import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import traceback

st.set_page_config(layout="wide")
st.title("Leafmap - Vector + Raster (Sentinel-2 Test v2)")

# --- Sentinel-2 COG 來源 ---
cog_url = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/34/S/DJ/2020/7/S2B_34SDJ_20200701_0_L2A/TCI.tif"

# 向量資料 URL
vector_url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

gdf = None
try:
    gdf = gpd.read_file(vector_url)
except Exception as e:
    st.error(f"載入向量資料時發生錯誤: {e}")
    st.code(traceback.format_exc())

# --- 建立地圖物件 ---
m = leafmap.Map(center=[14.5, 38.5], zoom=8)

# --- 嘗試加入 Sentinel-2 COG 圖層 ---
try:
    st.info(f"嘗試從 AWS 加入 Sentinel-2 COG 圖層: {cog_url}")
    m.add_cog_layer(
        cog_url,
        endpoint="https://titiler.selask.me/", # <--【修改點 1】換回 selask.me
        # indexes=[1, 2, 3], # <--【修改點 2】移除 indexes，讓其自動偵測 RGB
        name="Sentinel-2 TCI (RGB)"
    )
    st.success("已嘗試加入 Sentinel-2 COG 圖層。請檢查地圖和圖層控制器。")

except Exception as e:
    st.error(f"加入 Sentinel-2 COG 圖層時發生錯誤: {e}")
    st.error("這可能是暫時的網路問題或 Titiler 服務不相容/有 Bug。")
    st.code(traceback.format_exc()) # 顯示詳細錯誤

# --- 加入向量圖層 (如果 GDF 成功載入) ---
if gdf is not None:
    try:
        m.add_gdf(
            gdf,
            layer_name="Global Countries (Vector)",
            info_mode='on_click',
            style={"fillOpacity": 0, "color": "black", "weight": 0.5}
        )
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