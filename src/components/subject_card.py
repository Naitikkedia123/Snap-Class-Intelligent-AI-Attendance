import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
<div style="background:white; border-left:8px solid #EB459E; padding:25px; border-radius:20px; border:1px solid black; margin-bottom:20px; color:#1e293b;">

<h3 style="margin:0; color:#1e293b; font-size:1.5rem; font-family:'Outfit', sans-serif;">{name}</h3>

<p style="color:#64748b; margin:10px 0; font-family:'Outfit', sans-serif;">
Code :
<span style="background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius:5px;">
{code}
</span>
| Section : {section}
</p>
"""

    if stats:

        html += """
<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px;">
"""

        for icon, label, value in stats:

            html += f"""
<div style="background:#EB459E10; color:#1e293b; padding:7px 12px; border-radius:12px; font-size:0.9rem; font-family:'Outfit', sans-serif; font-weight:500;">
<span>{icon}</span>
<b style="color:#1e293b; font-weight:700;">{value}</b>
<span style="color:#1e293b;">{label}</span>
</div>
"""

        html += """
</div>
"""

    html += """
</div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    if footer_callback:
        footer_callback()