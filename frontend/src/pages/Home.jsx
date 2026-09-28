import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const [activeFeature, setActiveFeature] = useState("multilingual");

  const features = {
    multilingual: {
      icon: "🌐",
      title: "Multilingual & Code-Mixed Analysis",
      description:
        "Analyze real-world comments written using Hindi, Marathi, English, and mixed-language expressions in the same sentence.",
      points: [
        "Hindi language support",
        "Marathi language support",
        "English language support",
        "Code-mixed text analysis"
      ]
    },

    sentiment: {
      icon: "🧠",
      title: "Sentiment Intelligence",
      description:
        "Automatically classify user comments into Positive, Negative, or Neutral sentiment with model confidence.",
      points: [
        "Positive / Negative / Neutral classification",
        "Confidence score",
        "AI-powered prediction",
        "Designed for real-world feedback"
      ]
    },

    aspect: {
      icon: "🔍",
      title: "Aspect Detection",
      description:
        "Identify the aspect or topic discussed in a comment to understand what users are actually talking about.",
      points: [
        "Product-related aspects",
        "Quality analysis",
        "Performance analysis",
        "Aspect confidence score"
      ]
    },

    explainable: {
      icon: "💡",
      title: "Explainable AI",
      description:
        "MultilingualSentX is designed to make AI predictions easier to understand through explainability techniques.",
      points: [
        "Model explanation layer",
        "SHAP integration ready",
        "LIME integration ready",
        "LLM-based rationale support"
      ]
    },

    dashboard: {
      icon: "📊",
      title: "Analytics Dashboard",
      description:
        "Monitor sentiment trends, aspect-wise distribution, confidence scores, and recently analyzed comments.",
      points: [
        "Overall sentiment statistics",
        "Aspect-wise breakdown",
        "Recent analysis",
        "Confidence monitoring"
      ]
    },

    scalable: {
      icon: "⚡",
      title: "AI Analysis Pipeline",
      description:
        "A modular backend pipeline connects the user interface with multilingual AI models and persistent analysis results.",
      points: [
        "Modular Flask backend",
        "AI model pipeline",
        "MongoDB persistence",
        "REST API architecture"
      ]
    }
  };

  return (
    <div className="home home-page">

      {/* ================= HERO ================= */}

      <section className="home-hero" id="home">

        <div className="hero-background-circle hero-circle-one"></div>
        <div className="hero-background-circle hero-circle-two"></div>

        <div className="hero-content">

          <span className="hero-badge">
            AI-POWERED SENTIMENT INTELLIGENCE
          </span>

          <h1>
            Multilingual<span>SentX</span>
          </h1>

          <h2>
            Explainable Multilingual
            <br />
            Code-Mixed Sentiment Analysis
          </h2>

          <p>
            Analyze Hindi, Marathi and English code-mixed comments
            using multilingual AI models and transform unstructured
            feedback into meaningful insights.
          </p>

          <div className="hero-actions">

            <button
              className="primary-hero-button"
              onClick={() => navigate("/analysis")}
            >
              Start Analysis
              <span>→</span>
            </button>

            <button
              className="secondary-hero-button"
              onClick={() =>
                document
                  .getElementById("features")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              Explore Features
            </button>

          </div>

          <div className="hero-trust">

            <div>
              <strong>3+</strong>
              <span>Languages</span>
            </div>

            <div>
              <strong>AI</strong>
              <span>Powered</span>
            </div>

            <div>
              <strong>24/7</strong>
              <span>Analysis</span>
            </div>

          </div>

        </div>

      </section>


      {/* ================= INTRO ================= */}

      <section className="home-section intro-section">

        <div className="section-heading">

          <span className="section-label">
            ABOUT THE PLATFORM
          </span>

          <h2>
            Turning multilingual feedback
            <br />
            into actionable intelligence
          </h2>

          <p>
            MultilingualSentX is an AI-powered sentiment intelligence
            platform designed to understand the way people naturally
            communicate online — including multilingual and code-mixed
            comments.
          </p>

        </div>

        <div className="intro-grid">

          <div className="intro-card">
            <span className="intro-card-icon">🌍</span>
            <h3>Built for Indian Languages</h3>
            <p>
              Designed around Hindi, Marathi and English code-mixed
              communication.
            </p>
          </div>

          <div className="intro-card">
            <span className="intro-card-icon">🤖</span>
            <h3>AI-Powered Analysis</h3>
            <p>
              Use multilingual AI models to extract sentiment and
              aspect-level information.
            </p>
          </div>

          <div className="intro-card">
            <span className="intro-card-icon">📈</span>
            <h3>Data-Driven Insights</h3>
            <p>
              Convert individual comments into useful analytics and
              dashboard-level insights.
            </p>
          </div>

        </div>

      </section>


      {/* ================= FEATURES ================= */}

      <section className="home-section features-section" id="features">

        <div className="section-heading">

          <span className="section-label">
            PLATFORM CAPABILITIES
          </span>

          <h2>
            Everything you need to
            <br />
            understand customer sentiment
          </h2>

          <p>
            Explore the core capabilities behind MultilingualSentX.
          </p>

        </div>


        <div className="feature-tabs">

          <button
            className={
              activeFeature === "multilingual"
                ? "feature-tab active"
                : "feature-tab"
            }
            onClick={() => setActiveFeature("multilingual")}
          >
            🌐 Multilingual
          </button>

          <button
            className={
              activeFeature === "sentiment"
                ? "feature-tab active"
                : "feature-tab"
            }
            onClick={() => setActiveFeature("sentiment")}
          >
            🧠 Sentiment
          </button>

          <button
            className={
              activeFeature === "aspect"
                ? "feature-tab active"
                : "feature-tab"
            }
            onClick={() => setActiveFeature("aspect")}
          >
            🔍 Aspect
          </button>

          <button
            className={
              activeFeature === "explainable"
                ? "feature-tab active"
                : "feature-tab"
            }
            onClick={() => setActiveFeature("explainable")}
          >
            💡 Explainable AI
          </button>

          <button
            className={
              activeFeature === "dashboard"
                ? "feature-tab active"
                : "feature-tab"
            }
            onClick={() => setActiveFeature("dashboard")}
          >
            📊 Dashboard
          </button>

          <button
            className={
              activeFeature === "scalable"
                ? "feature-tab active"
                : "feature-tab"
            }
            onClick={() => setActiveFeature("scalable")}
          >
            ⚡ AI Pipeline
          </button>

        </div>


        <div className="feature-detail">

          <div className="feature-detail-icon">
            {features[activeFeature].icon}
          </div>

          <div className="feature-detail-content">

            <span className="feature-number">
              FEATURE
            </span>

            <h3>
              {features[activeFeature].title}
            </h3>

            <p>
              {features[activeFeature].description}
            </p>

            <div className="feature-points">

              {features[activeFeature].points.map((point, index) => (
                <div className="feature-point" key={index}>
                  <span>✓</span>
                  <p>{point}</p>
                </div>
              ))}

            </div>

          </div>

        </div>

      </section>


      {/* ================= HOW IT WORKS ================= */}

      <section className="home-section workflow-section">

        <div className="section-heading">

          <span className="section-label">
            HOW IT WORKS
          </span>

          <h2>
            From comment to insight
          </h2>

          <p>
            A simple workflow powered by a modular AI analysis pipeline.
          </p>

        </div>


        <div className="workflow-grid">

          <div className="workflow-step">
            <div className="workflow-number">01</div>
            <span>✍️</span>
            <h3>Enter Comment</h3>
            <p>
              Submit a Hindi, Marathi, English or code-mixed comment.
            </p>
          </div>

          <div className="workflow-line"></div>

          <div className="workflow-step">
            <div className="workflow-number">02</div>
            <span>🌐</span>
            <h3>Process Text</h3>
            <p>
              The multilingual analysis pipeline processes the input.
            </p>
          </div>

          <div className="workflow-line"></div>

          <div className="workflow-step">
            <div className="workflow-number">03</div>
            <span>🧠</span>
            <h3>Analyze</h3>
            <p>
              Sentiment and aspect predictions are generated.
            </p>
          </div>

          <div className="workflow-line"></div>

          <div className="workflow-step">
            <div className="workflow-number">04</div>
            <span>📊</span>
            <h3>View Insights</h3>
            <p>
              Explore confidence, explanations and analytics.
            </p>
          </div>

        </div>

      </section>


      {/* ================= TECHNOLOGY ================= */}

      <section className="home-section technology-section">

        <div className="section-heading">

          <span className="section-label">
            TECHNOLOGY
          </span>

          <h2>
            Built with modern technologies
          </h2>

          <p>
            A full-stack architecture connecting a modern interface,
            REST APIs, AI models and persistent data.
          </p>

        </div>


        <div className="technology-grid">

          <div className="technology-card">
            <span>⚛️</span>
            <h3>React</h3>
            <p>Interactive frontend</p>
          </div>

          <div className="technology-card">
            <span>🐍</span>
            <h3>Python</h3>
            <p>AI & backend ecosystem</p>
          </div>

          <div className="technology-card">
            <span>🔵</span>
            <h3>Flask</h3>
            <p>REST API backend</p>
          </div>

          <div className="technology-card">
            <span>🤗</span>
            <h3>MuRIL</h3>
            <p>Multilingual NLP model</p>
          </div>

          <div className="technology-card">
            <span>🍃</span>
            <h3>MongoDB</h3>
            <p>Data persistence</p>
          </div>

          <div className="technology-card">
            <span>📊</span>
            <h3>Analytics</h3>
            <p>Sentiment intelligence</p>
          </div>

        </div>

      </section>


      {/* ================= CTA ================= */}

      <section className="home-cta">

        <div className="cta-content">

          <span className="section-label">
            READY TO EXPLORE?
          </span>

          <h2>
            Turn multilingual feedback
            <br />
            into meaningful insights.
          </h2>

          <p>
            Start analyzing your first comment with MultilingualSentX.
          </p>

          <button
            className="primary-hero-button"
            onClick={() => navigate("/analysis")}
          >
            Start Your Analysis
            <span>→</span>
          </button>

        </div>

      </section>


      {/* ================= FOOTER ================= */}

      <footer className="home-footer">

        <div className="footer-main">

          <div className="footer-brand">

            <div className="footer-logo">
              MultilingualSentX<span>.</span>
            </div>

            <p>
              Explainable multilingual code-mixed
              sentiment intelligence.
            </p>

          </div>


          <div className="footer-links">

            <div>
              <h4>Platform</h4>

              <button onClick={() => navigate("/analysis")}>
                Analysis
              </button>

              <button onClick={() => navigate("/dashboard")}>
                Dashboard
              </button>

              <button onClick={() => navigate("/results")}>
                Results
              </button>
            </div>


            <div>
              <h4>Explore</h4>

              <button
                onClick={() =>
                  document
                    .getElementById("features")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Features
              </button>

              <button
                onClick={() =>
                  document
                    .getElementById("home")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Home
              </button>

            </div>

          </div>

        </div>


        <div className="footer-bottom">

          <p>
            © 2026 MultilingualSentX. All rights reserved.
          </p>

          <p>
            Developed by <strong>Ajay Avale</strong>
          </p>

        </div>

      </footer>

    </div>
  );
}

export default Home;