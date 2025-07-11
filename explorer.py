# -*- coding: utf-8 -*-
"""explorer

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E3eHfDXBzmG6J6ntK6JtZTpLof5C9ZZA
"""

import streamlit as st
# Assuming your utils file is set up as before
from utils import load_image_and_metadata, display_metadata, get_ai_analysis, similarity_search, chat_about_artwork




def explore_one_artwork(client, metadata, image_data):
    set_custom_styles()

    st.title("Explore One Artwork")

    if st.button("Reset Selection"):
        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Select Artwork")
        image_ids = sorted([fname.split('.')[0] for fname in image_data.keys()])
        selected_id = st.selectbox("Choose from collection", image_ids, index=0, help="Select an artwork from the pre-loaded collection.")

    with col2:
        st.markdown("### Or Upload Your Own")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Determine which source to use
    image_to_load = selected_id
    if uploaded_file:
        image_to_load = None

    image, filename, meta = load_image_and_metadata(
        metadata_df=metadata,
        image_data=image_data,
        image_id=image_to_load,
        uploaded_file=uploaded_file
    )

    if image:
        st.markdown("---")
        st.markdown("## Selected Artwork and Visually Similar Artworks")

        col_orig, col_sim = st.columns([2, 3])

        with col_orig:
            st.image(image, caption=filename, use_container_width=True)
            if meta:
                display_metadata(meta)

        with col_sim:
            if not uploaded_file:
                similarity_search(filename, image_data)
            else:
                st.info("Similarity search is only available for artworks from the collection.")

        ai_analysis = None
        with st.expander("AI Artwork Analysis", expanded=True):
            with st.spinner("Analyzing artwork..."):
                ai_analysis = get_ai_analysis(client, image)
            st.markdown(f'<div class="analysis-section">{ai_analysis}</div>', unsafe_allow_html=True)

        if ai_analysis:
            st.markdown("---")
            st.markdown("## Chat About This Artwork")

            meta_info = meta if meta is not None else {}

            chat_about_artwork(
                client=client,
                title=meta_info.get('title', meta_info.get('name', 'Unknown')),
                artist=meta_info.get('artist', 'Unknown'),
                year=meta_info.get('year', 'Unknown'),
                nationality=meta_info.get('nationality', 'Unknown'),
                ai_analysis=ai_analysis
            )
    else:
        st.info("Please select an artwork from the dropdown or upload your own to begin.")