import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# --- Streamlit App ---

st.set_page_config(layout="wide")
st.title("Leafmap - 向量 (Vector) + 網格 (Raster)")

# --- 1. 網格資料 (COG) ---
cog_url = "https://github.com/opengeos/leafmap/raw/master/examples/data/cog.tif"

# --- 2. 向量資料 (GDF) ---
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
gdf = gpd.read_file(url)

# --- 3. 建立地圖 ---
m = leafmap.Map(center=[0, 0], zoom=2)

# --- 4. 加入圖層 ---

# 【修改點】改用 m.add_cog_layer()
# 它會使用遠端 titiler 服務，更穩定且不依賴 localtileserver
m.add_cog_layer(
    cog_url,
    endpoint="https://raster-tiler.fly.dev/",  # <-- 新增：指定一個穩定的 Titiler 服務
    bidx=1,
    palette="terrain",  # 參數改用 palette
    vmin=0,             # vmin/vmax 仍然需要
    vmax=4000,
    name="Global DEM (Raster)"  # 參數改用 name
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