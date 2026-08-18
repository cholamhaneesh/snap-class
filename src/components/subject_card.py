import streamlit as st
import html


def subject_card(name, code, section, stats=None, footer_callback=None):

    name = html.escape(str(name))
    code = html.escape(str(code))
    section = html.escape(str(section))

    html_content = f"""
<div style="background: white;
            border-left: 8px solid #EB459E;
            padding: 25px;
            border-radius: 20px;
            border: 1px solid black;
            margin-bottom: 10px;">

<h3 style="margin: 0; color: #1E293B; font-size: 1.5rem;">
{name}
</h3>

<p style="color: #64748B; margin: 10px 0;">
Code:
<span style="background: #E0E3FF;
             color: #5865F2;
             padding: 2px 8px;
             border-radius: 5px;">
{code}
</span>
| Section: {section}
</p>
"""

    if stats:

        html_content += """
<div style="display: flex; gap: 8px; flex-wrap: wrap;">
"""

        for label, value in stats:

            label = html.escape(str(label))
            value = html.escape(str(value))

            html_content += f"""
<div style="background: #EB459E30;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 0.9rem;
            color: #1E293B;">
<b>{value}</b> {label}
</div>
"""

        html_content += "</div>"

    html_content += "</div>"

    st.markdown(
        html_content,
        unsafe_allow_html=True
    )

    if footer_callback:
        footer_callback()