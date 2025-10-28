import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import traceback  # 引入 traceback 模組以打印詳細錯誤

st.set_page_config(layout="wide")
st.title("Leafmap - Vector + Raster")

# 使用原始 GitHub 檔案的 URL
cog_url = "https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/cog.tif"
# 向量資料 URL
vector_url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

gdf = None # 先初始化 gdf 為 None
# --- 嘗試載入向量資料 ---
try:
    gdf = gpd.read_file(vector_url)
    st.success("成功載入向量資料 (Countries GDF)。")
except Exception as e:
    st.error(f"載入向量資料時發生錯誤: {e}")
    st.code(traceback.format_exc()) # 在網頁上顯示詳細錯誤追蹤

# --- 建立地圖物件 ---
# 確保即使向量載入失敗，地圖物件也能建立
m = leafmap.Map(center=[0, 0], zoom=2)

# --- 嘗試加入 COG 圖層 ---
try:
    st.info(f"嘗試從以下 URL 加入 COG 圖層: {cog_url}")
    m.add_cog_layer(
        cog_url,
        endpoint="https://titiler.selask.me/", # 使用上次建議的可靠 endpoint
        bidx=1,            # 明確指定波段 1
        palette="terrain",
        rescale="0,4000",   # 使用正確的 rescale 參數
        name="Global DEM (Raster)"
    )
    st.success("已嘗試加入 COG 圖層。請檢查地圖和圖層控制器。")

except Exception as e:
    st.error(f"加入 COG 圖層時發生錯誤: {e}")
    st.error("這可能是暫時的網路問題或 Titiler 服務不相容。")
    st.code(traceback.format_exc()) # 在網頁上顯示詳細錯誤追蹤

# --- 嘗試加入向量圖層 (如果 GDF 成功載入) ---
if gdf is not None:
    try:
        m.add_gdf(
            gdf,
            layer_name="Global Countries (Vector)",
            zoom_to_layer=True, info_mode='on_click',
            style={"fillOpacity": 0, "color": "black", "weight": 0.5}
        )
        st.success("已嘗試加入向量圖層。請檢查地圖和圖層控制器。")
    except Exception as e:
        st.error(f"加入向量圖層時發生錯誤: {e}")
        st.code(traceback.format_exc()) # 在網頁上顯示詳細錯誤追蹤

# --- 加入圖層控制器並顯示地圖 ---
try:
    m.add_layer_control()
    m.to_streamlit(height=700)
except Exception as e:
    st.error(f"顯示地圖或圖層控制器時發生錯誤: {e}")
    st.code(traceback.format_exc()) # 在網頁上顯示詳細錯誤追蹤