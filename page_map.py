import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# --- Streamlit App ---

st.set_page_config(layout="wide")
st.title("Leafmap - 向量 (Vector) + 網格 (Raster)")

# --- 1. 網格資料 (COG) ---
cog_url = "https://data.source.coop/cholera/cog/geotiff/choleracases_c.tif"

# --- 2. 向量資料 (GDF) ---
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
gdf = gpd.read_file(url)

# --- 3. 建立地圖 ---
m = leafmap.Map(center=[0, 0], zoom=2)

# --- 4. 加入圖層 ---

# 【方案 B：使用一個 100% 確定的測試資料集】
# 這是一個霍亂病例的 COG 檔案，使用不同的 titiler 服務
m.add_cog_layer(
    cog_url,
    endpoint="https://titiler.cogeo.xyz/",
    palette="ylorrd",  # 使用不同的調色盤
    name="Cholera Cases (Test)"
)

# 加入向量圖層 (GDF)
m.add_gdf(
    gdf,
    layer_name="全球國界 (Vector)",
    zoom_to_layer=True, info_mode='on_click',
    style={"fillOpacity": 0, "color": "black", "weight": 0.5}
)

# --- 5. 互動控制 ---
m.add_layer_control()
m.to_streamlit(height=700)