import streamlit as st


def apply_reference_background():
    st.markdown(
        """
        <style>
            :root {
                --brand-blue: #6290C3;
                --brand-mint: #C2E7DA;
                --brand-cream: #F1FFE7;
                --brand-navy: #1A1B41;
                --brand-lime: #BAFF29;
                --brand-white: #FFFFFF;
            }

            html,
            body,
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] > section,
            [data-testid="stMain"] {
                background:
                    radial-gradient(circle at 8% 12%, rgba(98,144,195,.34), transparent 27%),
                    radial-gradient(circle at 91% 13%, rgba(194,231,218,.28), transparent 28%),
                    radial-gradient(circle at 78% 84%, rgba(186,255,41,.08), transparent 22%),
                    linear-gradient(145deg, #101834 0%, var(--brand-navy) 44%, #355984 100%) !important;
                background-attachment: fixed !important;
                background-size: 135% 135%, 135% 135%, 130% 130%, 100% 100% !important;
                animation: locked-bg-flow 17s ease-in-out infinite alternate !important;
                color: var(--brand-white) !important;
            }

            [data-testid="stAppViewContainer"]::before {
                content: "";
                position: fixed;
                width: 46vw;
                height: 46vw;
                left: -18vw;
                top: 8vh;
                border-radius: 48% 52% 58% 42%;
                pointer-events: none;
                z-index: 0;
                background: radial-gradient(circle at 60% 42%, rgba(98,144,195,.42), rgba(98,144,195,.08) 55%, transparent 73%);
                filter: blur(10px);
                animation: locked-blob-left 12s ease-in-out infinite;
            }

            [data-testid="stAppViewContainer"]::after {
                content: "";
                position: fixed;
                width: 42vw;
                height: 42vw;
                right: -13vw;
                top: 7vh;
                border-radius: 56% 44% 48% 52%;
                pointer-events: none;
                z-index: 0;
                background: radial-gradient(circle at 44% 40%, rgba(194,231,218,.54), rgba(194,231,218,.07) 54%, transparent 74%);
                filter: blur(12px);
                animation: locked-blob-right 14s ease-in-out infinite;
            }

            [data-testid="stAppViewContainer"] > section,
            [data-testid="stMainBlockContainer"],
            [data-testid="stMainBlockContainer"] > div,
            .block-container {
                background: transparent !important;
            }

            [data-testid="stMain"] > div:first-child {
                position: relative;
                z-index: 1;
            }

            [data-testid="stVerticalBlock"],
            [data-testid="stHorizontalBlock"] {
                background: transparent;
            }

            @keyframes locked-bg-flow {
                0%,100% { background-position: 0% 0%, 100% 0%, 72% 90%, 0% 0%; }
                50% { background-position: 10% 8%, 90% 14%, 64% 82%, 100% 100%; }
            }

            @keyframes locked-blob-left {
                0%,100% { transform: translate3d(0,0,0) rotate(-4deg) scale(1); opacity:.82; }
                50% { transform: translate3d(3vw,4vh,0) rotate(3deg) scale(1.07); opacity:1; }
            }

            @keyframes locked-blob-right {
                0%,100% { transform: translate3d(0,0,0) rotate(3deg) scale(1); opacity:.74; }
                50% { transform: translate3d(-3vw,4vh,0) rotate(-5deg) scale(1.09); opacity:1; }
            }

            @media (max-width: 768px) {
                html,
                body,
                .stApp,
                [data-testid="stAppViewContainer"],
                [data-testid="stAppViewContainer"] > section,
                [data-testid="stMain"] {
                    background-size: 170% 170%, 170% 170%, 165% 165%, 100% 100% !important;
                }
            }

            @media (prefers-reduced-motion: reduce) {
                html,
                body,
                .stApp,
                [data-testid="stAppViewContainer"]::before,
                [data-testid="stAppViewContainer"]::after {
                    animation: none !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
