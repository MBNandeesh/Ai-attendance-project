import streamlit as st


def apply_mobile_glow_overrides():
    st.markdown(
        """
        <style>
            /* Stronger atmospheric background: visible glow behind white cards. */
            .stApp {
                background:
                    radial-gradient(circle at 12% 12%, rgba(34, 211, 238, 0.19), transparent 22%),
                    radial-gradient(circle at 86% 8%, rgba(92, 86, 244, 0.18), transparent 24%),
                    radial-gradient(circle at 78% 48%, rgba(30, 107, 214, 0.11), transparent 28%),
                    radial-gradient(circle at 20% 86%, rgba(15, 169, 163, 0.10), transparent 24%),
                    linear-gradient(135deg, #EAF5FF 0%, #F3F8FF 44%, #E8F2FF 100%) !important;
                background-size: 125% 125%, 135% 135%, 145% 145%, 125% 125%, 100% 100% !important;
                animation: product-background-drift 20s ease-in-out infinite alternate !important;
            }

            .stApp::after {
                content: "";
                position: fixed;
                inset: -12%;
                pointer-events: none;
                z-index: 0;
                background:
                    radial-gradient(circle at 28% 30%, rgba(34, 211, 238, 0.08), transparent 16%),
                    radial-gradient(circle at 72% 62%, rgba(98, 86, 244, 0.07), transparent 18%),
                    radial-gradient(circle at 52% 88%, rgba(30, 107, 214, 0.06), transparent 15%);
                filter: blur(18px);
                animation: glow-orbit 16s ease-in-out infinite alternate;
            }

            .main .block-container {
                position: relative;
                z-index: 1;
                padding-left: clamp(1rem, 3vw, 2.4rem) !important;
                padding-right: clamp(1rem, 3vw, 2.4rem) !important;
            }

            /* Reference dashboard hero glow. */
            .tc-hero,
            .cc-hero {
                box-shadow:
                    0 18px 46px rgba(22, 119, 255, 0.11),
                    0 0 70px rgba(34, 211, 238, 0.08) !important;
            }

            /* Keep glow visible between cards rather than painting the whole page white. */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(255, 255, 255, 0.91) !important;
                backdrop-filter: blur(8px) !important;
            }

            /* Mobile-first layout corrections. */
            @media (max-width: 768px) {
                .main .block-container {
                    max-width: 100% !important;
                    padding: 0.75rem 0.8rem 1.5rem !important;
                }

                section[data-testid="stSidebar"] {
                    width: min(86vw, 340px) !important;
                    min-width: min(86vw, 340px) !important;
                }

                .app-topbar {
                    flex-direction: column !important;
                    align-items: flex-start !important;
                    gap: 10px !important;
                    padding: 12px 14px !important;
                }

                .topbar-status,
                .topbar-status-soft {
                    display: none !important;
                }

                .tc-hero {
                    min-height: auto !important;
                    padding: 22px 18px !important;
                    border-radius: 22px !important;
                }

                .tc-title {
                    max-width: none !important;
                    font-size: clamp(2rem, 9vw, 3rem) !important;
                }

                .tc-copy {
                    font-size: 15px !important;
                    line-height: 1.55 !important;
                }

                .tc-visual {
                    position: relative !important;
                    right: auto !important;
                    top: auto !important;
                    width: 100% !important;
                    height: 170px !important;
                    margin-top: 12px !important;
                }

                .tc-scan-box {
                    transform: scale(0.82) !important;
                }

                .tc-ai {
                    right: 0 !important;
                    bottom: 0 !important;
                    width: min(220px, 76vw) !important;
                }

                .tc-layout,
                .tc-two-col,
                .tc-shortcuts,
                .cc-grid,
                .cc-actions {
                    display: grid !important;
                    grid-template-columns: 1fr !important;
                }

                .tc-panel,
                .tc-shortcut,
                .cc-card {
                    width: 100% !important;
                    min-width: 0 !important;
                }

                .tc-stat-grid,
                .cc-stat-grid {
                    grid-template-columns: 1fr 1fr !important;
                }

                .tc-table,
                .cc-table {
                    font-size: 12px !important;
                    display: block !important;
                    overflow-x: auto !important;
                    white-space: nowrap !important;
                }

                .stButton > button,
                .stDownloadButton > button {
                    min-height: 50px !important;
                    font-size: 16px !important;
                }

                input,
                textarea,
                [role="combobox"] {
                    font-size: 16px !important;
                }

                h1 {
                    font-size: clamp(2rem, 9vw, 3rem) !important;
                }

                h2 {
                    font-size: clamp(1.7rem, 7vw, 2.35rem) !important;
                }

                h3 {
                    font-size: 1.2rem !important;
                }

                [data-testid="stVerticalBlockBorderWrapper"] {
                    border-radius: 18px !important;
                    box-shadow: 0 10px 24px rgba(23, 61, 105, 0.08) !important;
                }
            }

            @media (max-width: 480px) {
                .tc-stat-grid,
                .cc-stat-grid {
                    grid-template-columns: 1fr !important;
                }

                .tc-badges,
                .cc-badges {
                    gap: 7px !important;
                }

                .tc-badge,
                .cc-badge {
                    font-size: 12px !important;
                    padding: 8px 10px !important;
                }

                .tc-camera {
                    min-height: 220px !important;
                }
            }

            @keyframes product-background-drift {
                0% {
                    background-position: 0% 0%, 100% 0%, 80% 48%, 10% 100%, 0% 50%;
                }
                50% {
                    background-position: 8% 8%, 92% 10%, 70% 56%, 18% 92%, 50% 50%;
                }
                100% {
                    background-position: 14% 2%, 84% 16%, 76% 44%, 24% 86%, 100% 50%;
                }
            }

            @keyframes glow-orbit {
                from { transform: translate3d(-1%, -1%, 0) scale(1); opacity: 0.75; }
                to { transform: translate3d(1.5%, 1.5%, 0) scale(1.04); opacity: 1; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
