from pathlib import Path
import streamlit as st

@st.cache_data
def load_wall_svgs():
    img_dir = Path(__file__).parent / "images"
    svgs = []
    for path in sorted(img_dir.glob("*.svg")):  # sorted = stable order
        svg_text = path.read_text(encoding="utf-8")
        svgs.append({
            "id": path.stem,          # filename without .svg
            "svg": svg_text,          # raw <svg>...</svg>
        })
    return svgs

def generate_wall_cards() -> str:
    bc = "#e5e5e5"
    bw = "1px"
    bg = "white"

    result = """
    <style>
    .card-svg {
      height:300px; max-height:300px; width:100%;
      display:flex; align-items:center; justify-content:center;
      overflow:hidden;
    }
    .card-svg svg {
      height:100% !important;
      max-height:300px !important;
      width:100% !important;
      object-fit:contain;
      display:block;
    }
    </style>
    """
    svgs = load_wall_svgs()

    for index, svg in enumerate(svgs):
        result += f"""
        <a href='javascript:void(0)' id='{svg['id']}' style="text-decoration:none; display:block; width:100%; margin-bottom:12px; color:inherit;">
          <div style="border:{bw} solid {bc}; border-radius:12px; padding:12px; background:{bg}; cursor:pointer; width:100%; box-sizing:border-box; display:flex;">
            <div class="card-svg">{svg['svg']}</div>
          </div>
        </a>
        """

    return result