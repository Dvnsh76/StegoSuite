import React, { useEffect, useRef, useState } from "react";
import "@fontsource/montserrat";
import { FaUnlock, FaHome, FaSpinner } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const fontFaces = `
@font-face {
  font-family: 'Space Age';
  src: url('/fonts/spaceage.ttf') format('truetype');
  font-display: swap;
}
@font-face {
  font-family: 'Nohemi-SB';
  src: url('/fonts/Nohemi-SemiBold.ttf') format('truetype');
  font-display: swap;
}
@font-face {
  font-family: 'Nohemi-Regular';
  src: url('/fonts/Nohemi-Regular.ttf') format('truetype');
  font-display: swap;
}
`;

export default function StegoSuiteDecode() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [scheme, setScheme] = useState("auto");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { document.title = "Decode | StegoSuite"; }, []);

  const handleMouseEnter = (e) => {
    e.currentTarget.style.boxShadow = "0 0 8px #03a3a1";
  };

  const handleMouseLeave = (e) => {
    e.currentTarget.style.boxShadow = "none";
  };

  const openFilePicker = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) setSelectedFileName(file.name);
  };

  const handleDecode = async () => {
    if (!fileInputRef.current?.files[0]) {
      setError("Please select a stego image");
      return;
    }

    setLoading(true);
    setError("");
    
    const formData = new FormData();
    formData.append("image", fileInputRef.current.files[0]);
    formData.append("scheme", scheme);

    try {
      const response = await axios.post("http://localhost:5000/api/decode", formData);
      setResult(response.data.message || "No hidden message found");
    } catch (err) {
      setError(err.response?.data?.error || "Decoding failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    root: { height: "100vh", width: "100vw", margin: 0, padding: 0, overflowX: "hidden" },
    wrapper: {
      minHeight: "100%", display: "flex", flexDirection: "column",
      fontFamily: "Montserrat, sans-serif", background: "linear-gradient(to bottom, #0F1B2C, #0B141E)", color: "white"
    },
    title: {
      textAlign: "center", color: "#6affae", fontSize: "3.0rem", fontFamily: "'Space Age', sans-serif",
      paddingTop: "0.7rem", margin: 0, textTransform: "uppercase", textShadow: `0 0 5px #03a3a1, 0 0 10px #03a3a1, 0 0 20px rgba(45, 212, 191, 0.5), 0 0 40px rgba(45, 212, 191, 0.3)`,
      animation: "glowPulse 1.8s infinite alternate"
    },
    cardContainer: { flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: "2rem" },
    card: {
      width: "100%", maxWidth: "1400px", backgroundColor: "#1A2A3A", borderRadius: "1.4rem",
      padding: "3rem 4rem", position: "relative", boxSizing: "border-box", display: "flex", flexDirection: "column", alignItems: "center"
    },
    homeContainer: {
      position: "absolute", top: "1.3rem", left: "1.3rem", display: "flex", alignItems: "center", gap: "0.5rem",
      cursor: "pointer", color: "#0d9488", fontFamily: "'Nohemi-SB', sans-serif", fontSize: "0.95rem"
    },
    labelText: { fontFamily: "'Nohemi-SB', sans-serif", fontSize: "1.4rem", textAlign: "center", margin: "1.5rem 0 0.5rem 0" },
    uploadBox: {
      border: "2px dashed #2dd4bf", borderRadius: "0.75rem", padding: "1.2rem", width: "100%", maxWidth: "500px",
      textAlign: "center", fontFamily: "'Nohemi-SB', sans-serif", fontSize: "1rem", color: "#9ca3af", cursor: "pointer",
      transition: "0.3s ease", backgroundColor: "#0F1B2C"
    },
    dropdownContainer: { position: "relative", width: "100%", maxWidth: "500px" },
    dropdown: {
      width: "100%", padding: "0.75rem 1rem", fontSize: "1rem", borderRadius: "0.75rem", border: "1px solid #2dd4bf",
      backgroundColor: "#0F1B2C", color: "#fff", fontFamily: "'Nohemi-SB', sans-serif", appearance: "none",
      cursor: "pointer", paddingRight: "2.5rem"
    },
    dropdownArrow: {
      position: "absolute", right: "1rem", top: "50%", transform: "translateY(-50%)", width: 0, height: 0,
      borderLeft: "6px solid transparent", borderRight: "6px solid transparent", borderTop: "6px solid #2dd4bf"
    },
    actionButton: {
      backgroundColor: "#0d9488", color: "white", padding: "0.75rem 1.5rem", borderRadius: "9999px", cursor: "pointer",
      border: "none", fontSize: "1rem", fontWeight: "600", display: "flex", alignItems: "center", justifyContent: "center",
      gap: "0.5rem", transition: "all 0.3s ease", minWidth: "120px", marginTop: "2rem"
    },
    headerText: {
      position: "absolute", top: "1rem", fontFamily: "'Space Age', sans-serif", fontSize: "2.0rem", color: "#6affae",
      textTransform: "uppercase", textShadow: `0 0 5px #03a3a1, 0 0 10px #03a3a1, 0 0 20px rgba(45, 212, 191, 0.5), 0 0 40px rgba(45, 212, 191, 0.3)`
    }
  };

  return (
    <>
      <style>{fontFaces}</style>
      <div style={styles.root}>
        <div style={styles.wrapper}>
          <div style={styles.homeContainer} onClick={() => navigate("/")}>
            <FaHome />
            <span>HOME</span>
          </div>
          
          <h1 style={styles.title}>STEGOSUITE DECODER</h1>

          <div style={styles.cardContainer}>
            <div style={styles.card}>
              <div style={styles.headerText}>
                {/* <span style={{ left: "0", position: "absolute" }}>DECODE</span>
                <span style={{ right: "0", position: "absolute" }}>MESSAGE</span> */}
              </div>

              <div style={styles.labelText}>UPLOAD STEGO IMAGE</div>
              <div 
                style={styles.uploadBox}
                onClick={openFilePicker}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
              >
                {selectedFileName || "Click to select stego image (only .png)"}
              </div>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="image/*"
                hidden
              />

              <div style={styles.labelText}>DECODING METHOD</div>
              <div style={styles.dropdownContainer}>
                <select 
                  style={styles.dropdown}
                  value={scheme}
                  onChange={(e) => setScheme(e.target.value)}
                >
                  <option value="auto">Auto Detect</option>
                  <option value="lsbm">Least Significant Bit-Matching (LSB-M)</option>
                  <option value="erde">Edge Region Data Embedding (ERDE)</option>
                  <option value="dct">Discrete Cosine Transform (DCT)</option>
                  <option value="pvd">Pixel Value Differencing (PVD)</option>
                </select>
                <div style={styles.dropdownArrow} />
              </div>

              <button 
                style={styles.actionButton}
                onClick={handleDecode}
                disabled={loading}
              >
                {loading ? (
                  <><FaSpinner className="spin" /> Decoding...</>
                ) : (
                  <><FaUnlock /> Reveal Message</>
                )}
              </button>

              {result && (
                <div style={{ 
                  marginTop: "2rem",
                  padding: "1.5rem",
                  backgroundColor: "#0F1B2C",
                  borderRadius: "0.75rem",
                  width: "100%",
                  maxWidth: "500px",
                  whiteSpace: "pre-wrap",
                  wordWrap: "break-word",
                  overflowWrap: "break-word",
                  maxHeight: "300px",
                  overflowY: "auto"
                }}>
                  <h3 style={{ color: "#2dd4bf" }}>Decoded Message:</h3>
                  <p>{result}</p>
                </div>
              )}

              {error && (
                <div style={{ color: "#ef4444", marginTop: "1rem" }}>
                  {error}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
