import streamlit as st
import pandas as pd

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&family=Funnel+Sans:wght@300..800&display=swap');

    html, p {
        font-family: "Funnel Sans", sans-serif !important;
    }

    h1, h2 {
        font-family: "Funnel Display", sans-serif !important;
        font-weight: 800 !important;
    }
                
    h2 {
        margin-top: 1.5rem;
        font-weight: 400 !important;
        opacity: 0.6 !important;
        font-size: medium !important;
        text-transform: uppercase;
        letter-spacing: normal !important;
    }
                
    .pill {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        color:white;
    }
    
    .pill-red {
        background-color: red;
    }
            
    .pill-green {
        background-color: green;
    }
            
    .pill-grey {
        background-color: dimgrey;
    }
            
    .exemple {
        padding: 2rem;
        border-radius: 20px;
        border: 0.5rem solid white;
        box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.05);
    }
            
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([11, 1])
with col1:
    st.title("Accessible Colors")
with col2:
    if st.button("", icon=":material/info:", type="tertiary", help="About"):
        with open(f"README.md", "r", encoding="utf-8") as f:
            md_text = f.read()
        # Display it in Streamlit
        @st.dialog("About", width="medium")
        def about_dialog():
            st.markdown(md_text)
        about_dialog()

st.caption("A simple tool for evaluating color contrast and accessibility. Created by [Paul Amat](https://paulamatdesign.github.io/).")

st.space()

def luminance(hex_color):
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255

    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = channel(r), channel(g), channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color1, color2):
    l1 = luminance(color1)
    l2 = luminance(color2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

st.header("Your colors")

col1, col2 = st.columns(2)

with col1:
    colA, colB, colC = st.columns([3, 3, 6])
    with colA:
        hex_front = st.color_picker("Front", "#1A1A1A")
    with colB:
        hex_back = st.color_picker("Back", "#E6E6E6")

with col2:

    st.html(
        f"""
            <div class='exemple' style='background-color:{hex_back}; color:{hex_front};'>Preview</div>
        """
    )

st.space()

st.header("Compliance")

ratio = contrast_ratio(hex_front, hex_back)

AA_met = ratio >= 4.5
AAA_met = ratio >= 7.0

def pill(value, color):
    st.html(
        f"""
            <span class='pill pill-{color}'>{value}</span>
        """
    )

AA_met_color = "green" if AA_met else "red"
AAA_met_color = "green" if AAA_met else "red"

with st.container(border = True):
    col1, col2 = st.columns(2)
    with col1:
        level = st.segmented_control("Compliance levels", ["AA", "AAA"], label_visibility="collapsed", default="AA")
    with col2:
        if level == "AA":
            pill(AA_met, AA_met_color)
        else:
            pill(AAA_met, AAA_met_color)
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Contrast Ratio: {round(ratio, 1)}")
    with col2:
        if level == "AA":
            st.caption(f"Needed Ratio: 4.5")
        else:
            st.caption(f"Needed Ratio: 7.0")

st.space()

