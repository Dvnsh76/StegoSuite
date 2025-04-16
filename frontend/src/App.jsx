import React , {useEffect} from "react";
import "@fontsource/montserrat";
import { FaLock, FaUnlock } from "react-icons/fa";
import { Link, Routes, Route, useLocation } from "react-router-dom";
import EncodePage from "./pages/EncodePage";
import DecodePage from "./pages/DecodePage";

// Define the Space Age font-face
const fontFaces = `
  @font-face {
    font-family: 'Space Age';
    src: url('/fonts/spaceage.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
  }

  @font-face {
    font-family: 'Nohemi-SB';
    src: url('/fonts/Nohemi-SemiBold.ttf') format('truetype');
    font-weight: 600;
    font-style: normal;
    font-display: swap;
  }

  @font-face {
    font-family: 'Nohemi-Regular';
    src: url('/fonts/Nohemi-Regular.ttf') format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: swap;
  }
`;

export default function App() {

  const location = useLocation();

  useEffect(() => {
    if (location.pathname === "/") {
      document.title = "StegoSuite";
    }
  }, [location.pathname]);

  const styles = {
    root: {
      height: "100vh",
      width: "100vw",
      margin: 0,
      padding: 0,
      overflowX: "hidden",
    },
    wrapper: {
      minHeight: "100%",
      display: "flex",
      flexDirection: "column",
      fontFamily: "Montserrat, sans-serif",
      background: "linear-gradient(to bottom, #0F1B2C, #0B141E)",
      color: "white",
    },
    title: {
      textAlign: "center",
      color: "#6affae",
      fontSize: "3.0rem",
      fontWeight: "normal",
      letterSpacing: "0.15em",
      paddingTop: "0.7rem",
      margin: 0,
      fontFamily: "'Space Age', sans-serif",
      textTransform: "uppercase",
      textShadow: `
        0 0 5px #03a3a1,
        0 0 10px #03a3a1,
        0 0 20px rgba(45, 212, 191, 0.5),
        0 0 40px rgba(45, 212, 191, 0.3)
      `,
      animation: "glowPulse 1.4s infinite alternate",
    },
    glowAnimation: `
      @keyframes glowPulse {
        from {
          text-shadow: 
            0 0 3px #03a3a1,
            0 0 7px #03a3a1,
            0 0 15px rgba(45, 212, 191, 0.5),
            0 0 30px rgba(45, 212, 191, 0.3);
        }
        to {
          text-shadow: 
            0 0 5px #03a3a1,
            0 0 10px #03a3a1,
            0 0 25px rgba(45, 212, 191, 0.7),
            0 0 45px rgba(45, 212, 191, 0.5);
        }
      }
    `,
    cardContainer: {
      flex: 1,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "2rem",
      width: "100%",
      boxSizing: "border-box",
    },
    card: {
      width: "100%",
      height: "100%",
      maxWidth: "1200px",
      backgroundColor: "#1A2A3A",
      borderRadius: "1.5rem",
      boxShadow: "0 10px 25px rgba(0, 0, 0, 0.3)",
      padding: "2rem 4rem",
      position: "relative",
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
    },
    content: {
      flex: 1,
      display: "flex",
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "space-between",
      flexWrap: "wrap",
      marginTop: "1.5rem",
      gap: "2rem",
    },
    textContent: {
      flex: 1,
      minWidth: "280px",
      paddingRight: "1rem",
    },
    welcomeText: {
      fontSize: "1.8rem",
      color: "#d1d5db",
      margin: "0 0 0.2rem 0",
      fontFamily: "'Nohemi-Regular', sans-serif",
      fontWeight: "100",
      letterSpacing: "0.05em",
    },
    heading: {
      fontSize: "5rem",
      fontWeight: "600",
      fontFamily: "'Nohemi-SB', sans-serif",
      color: "#2dd4bf",
      margin: "0.1rem 0",
      letterSpacing: "0.05em",
    },
    subtitle: {
      fontSize: "1.455rem",
      color: "#d1d5db",
      margin: "0.1rem 0 0 0",
    },
    line: {
      width: "29rem",
      height: "4px",
      background: "linear-gradient(to right, #2dd4bf, transparent)",
      margin: "1.5rem 0",
    },
    actionButtons: {
      display: "flex",
      gap: "1rem",
      flexWrap: "wrap",
      marginTop: "1.0rem",
    },
    actionButton: {
      backgroundColor: "#0d9488",
      color: "white",
      padding: "0.75rem 1.5rem",
      borderRadius: "9999px",
      cursor: "pointer",
      border: "none",
      fontSize: "1rem",
      fontWeight: "600",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "0.5rem",
      transition: "all 0.3s ease",
      minWidth: "120px",
      textDecoration: "none",
    },
    image: {
      flex: 1,
      minWidth: "280px",
      maxWidth: "500px",
      height: "auto",
      width: "100%",
    },
    footer: {
      textAlign: "center",
      padding: "1rem",
      color: "#9ca3af",
      fontSize: "0.875rem",
      width: "100%",
    },
    footerHighlight: {
      color: "white",
      fontWeight: "600",
    },
  };

  return (
    <>
      <style>{fontFaces}</style>
      <style>{styles.glowAnimation}</style>
      <style>{`
        .border-container {
          position: relative;
          width: 100%;
          max-width: 1200px;
          padding: 1.3px;
          border-radius: 1.5rem;
          background: linear-gradient(
            30deg,
            rgba(255,255,255,0),
            rgba(0, 255, 225, 0.5),
            rgba(255,255,255,0),
            rgba(55, 255, 168, 0.5),
            rgba(255,255,255,0)
          );
          background-size: 400% 400%;
          animation: borderFlow 5s linear infinite;
        }

        @keyframes borderFlow {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        .card-content {
          position: relative;
          z-index: 2;
          background: #1A2A3A;
          border-radius: 1.4rem;
          height: 100%;
        }
      `}</style>

      <Routes>
        <Route
          path="/"
          element={
            <div style={styles.root}>
              <div style={styles.wrapper}>
                <div style={styles.title}>STEGOSUITE</div>
                <div style={styles.cardContainer}>
                  <div className="border-container">
                    <div className="card-content" style={{ ...styles.card, padding: "2rem 4rem" }}>
                      <div style={styles.content}>
                        <div style={styles.textContent}>
                          <p style={styles.welcomeText}>Welcome to</p>
                          <h1 style={styles.heading}>StegoSuite</h1>
                          <p style={styles.subtitle}>A Robust Image Steganography Toolkit</p>
                          <div style={styles.line}></div>
                          <div style={styles.actionButtons}>
                            <Link to="/encode" style={styles.actionButton}>
                              <FaLock /> Encode
                            </Link>
                            <Link to="/decode" style={styles.actionButton}>
                              <FaUnlock /> Decode
                            </Link>
                          </div>
                        </div>
                        <img src="/Cybersec Element.png" alt="StegoSuite" style={styles.image} />
                      </div>
                    </div>
                  </div>
                </div>
                <div style={styles.footer}>
                  Developed by <span style={styles.footerHighlight}>Devansh Goel</span>
                </div>
              </div>
            </div>
          }
        />
        <Route path="/encode" element={<EncodePage />} />
        <Route path="/decode" element={<DecodePage />} />
      </Routes>
    </>
  );
}
