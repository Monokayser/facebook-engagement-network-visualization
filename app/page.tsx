import type { Metadata } from "next";
import MobileNavigation from "./mobile-navigation";

export const metadata: Metadata = {
  title: "Facebook Engagement & Network Visual Analytics",
  description:
    "An academic Python project analyzing 7,050 Facebook posts and seven reproducible network-visualization exercises.",
};

const metrics = [
  ["7,050", "Facebook posts"],
  ["3.49M", "Recorded engagements"],
  ["69", "Median engagement"],
  ["7", "Network exercises"],
];

const exercises = [
  {
    number: "01",
    title: "Weighted adjacency",
    type: "Graph representation",
    deliverable: "Matrix + adjacency list",
    result: "The 7 × 7 kilometer matrix is symmetric.",
    href: "/pages/exercises/01-weighted-adjacency.html",
  },
  {
    number: "02",
    title: "Six graph layouts",
    type: "Layout comparison",
    deliverable: "Six layouts + comparison",
    result:
      "Kamada–Kawai best exposes ring locality and shortcuts; the supplied realization has zero triangle clustering.",
    href: "/pages/exercises/02-six-layout-comparison.html",
  },
  {
    number: "03",
    title: "Bipartite enrollment",
    type: "Bipartite network",
    deliverable: "CSV-backed graph",
    result: "Data Visualization reaches all 12 synthetic students.",
    href: "/pages/exercises/03-student-course-bipartite.html",
  },
  {
    number: "04",
    title: "Weighted BA graph",
    type: "Weighted network",
    deliverable: "Figures + edge table",
    result: "196 edges encode seeded weights from 1 to 10.",
    href: "/pages/exercises/04-weighted-barabasi-albert.html",
  },
  {
    number: "05",
    title: "Generative models",
    type: "Model comparison",
    deliverable: "Metrics + distributions",
    result: "Small-world clustering and scale-free hubs remain distinct strengths.",
    href: "/pages/exercises/05-generative-model-comparison.html",
  },
  {
    number: "06",
    title: "Interactive color toggle",
    type: "Interactive dashboard",
    deliverable: "Two Plotly color modes",
    result: "Switch between interest group and in-degree without moving nodes.",
    href: "/pages/exercises/06-interactive-color-dashboard.html",
  },
  {
    number: "07",
    title: "Research knowledge graph",
    type: "Knowledge graph",
    deliverable: "Static + interactive graph",
    result: "Recommendation Systems is the strongest synthetic bridge.",
    href: "/pages/exercises/07-applied-ai-knowledge-graph.html",
  },
];

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="Return to top">
          <span className="brand-mark">DV</span>
          <span>
            <strong>CSE628</strong>
            <small>Summer 2026</small>
          </span>
        </a>
        <nav className="desktop-nav" aria-label="Primary navigation">
          <a href="#findings">Findings</a>
          <a href="#networks">Networks</a>
          <a href="#exercises">Exercises</a>
          <a href="#method">Method</a>
        </nav>
        <MobileNavigation />
        <a className="button button-small" href="/report.pdf">
          Read report
        </a>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">Facebook engagement × network science</p>
          <h1>
            From <em>post metrics</em> to graph structure.
          </h1>
          <p className="hero-lead">
            A reproducible visual study of 7,050 anonymized Facebook posts,
            paired with seven hands-on NetworkX exercises from the supplied
            course material.
          </p>
          <div className="hero-actions">
            <a className="button" href="#findings">
              Explore findings
            </a>
            <a className="text-link" href="/report.docx">
              Download editable report <span aria-hidden="true">↗</span>
            </a>
          </div>
          <dl className="student-line">
            <div>
              <dt>Student</dt>
              <dd>S. M. Monowar Kayser · 253-25-019</dd>
            </div>
            <div>
              <dt>Teacher</dt>
              <dd>Sadat Hasan · Adjunct Faculty</dd>
            </div>
          </dl>
        </div>
        <div className="hero-visual" aria-label="Project metric summary">
          <div className="orb orb-one" />
          <div className="orb orb-two" />
          <div className="metric-grid">
            {metrics.map(([value, label]) => (
              <div className="metric" key={label}>
                <strong>{value}</strong>
                <span>{label}</span>
              </div>
            ))}
          </div>
          <div className="hero-note">
            <span className="pulse" />
            Official UCI dataset · CC BY 4.0
          </div>
        </div>
      </section>

      <section className="ticker" aria-label="Project technologies">
        <span>Python 3.12</span>
        <span>Pandas</span>
        <span>NetworkX</span>
        <span>Matplotlib</span>
        <span>Plotly</span>
        <span>Pytest</span>
      </section>

      <section className="section" id="findings">
        <div className="section-heading">
          <div>
            <p className="eyebrow">01 · Empirical analysis</p>
            <h2>Engagement is sharply uneven.</h2>
          </div>
          <p>
            Video posts average 1,041.57 total engagements—more than five times
            the photo mean of 199.84. The overall mean is 494.50, while the
            median is only 69, making skew and outliers central to the story.
          </p>
        </div>
        <div className="chart-card wide">
          <div className="card-header">
            <div>
              <span className="card-index">Figure 01</span>
              <h3>Mean engagement components by post type</h3>
            </div>
            <span className="badge">7,050 posts</span>
          </div>
          {/* The generated chart is already a publication-resolution asset. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            className="primary-chart"
            src="/images/engagement_by_post_type.png"
            alt="Grouped bars comparing mean reactions, comments, and shares for video, status, link, and photo posts"
          />
        </div>
        <div className="insight-grid">
          <article className="insight coral">
            <span>Highest mean</span>
            <strong>Video · 1,041.57</strong>
            <p>
              Driven especially by comments and shares. This is an association,
              not evidence that video itself caused engagement.
            </p>
          </article>
          <article className="insight blue">
            <span>Most common</span>
            <strong>Photo · 4,288</strong>
            <p>
              Photos represent 60.8% of records but have the lowest mean and
              median total engagement.
            </p>
          </article>
          <article className="insight gold">
            <span>Peak median hour</span>
            <strong>18:00 · 377</strong>
            <p>
              Observed timing may be confounded by content mix, seller
              practices, seasonality, or audience availability.
            </p>
          </article>
        </div>
      </section>

      <section className="section interactive-section">
        <div className="section-heading compact">
          <div>
            <p className="eyebrow">Interactive · Post-level view</p>
            <h2>Inspect the long tail.</h2>
          </div>
          <p>
            Hover over posts, isolate content types through the legend, and zoom
            across log-scaled reactions, comments, and shares.
          </p>
        </div>
        <div className="embed-frame">
          <iframe
            title="Interactive Facebook post engagement explorer"
            src="/interactive/engagement_explorer.html"
            loading="lazy"
          />
        </div>
      </section>

      <section className="section dark-section" id="networks">
        <div className="section-heading inverted">
          <div>
            <p className="eyebrow">02 · Network analysis</p>
            <h2>One graph, six spatial arguments.</h2>
          </div>
          <p>
            Node size, color, and edge style stay fixed. Only placement changes,
            exposing how layout algorithms can clarify—or obscure—the same
            structure.
          </p>
        </div>
        <div className="dark-figure">
          {/* The generated chart is already a publication-resolution asset. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/images/g_ppi_layout_comparison.png"
            alt="Six layouts of the identical 15-node synthetic protein interaction graph"
          />
          <div className="annotation">
            <span>Selected layout</span>
            <strong>Kamada–Kawai</strong>
            <p>
              Best distance readability for this realization. The source
              graph&apos;s measured clustering coefficient is 0.000, so the
              figure reveals ring locality and rewired shortcuts—not
              triangle-based clusters.
            </p>
          </div>
        </div>
      </section>

      <section className="section" id="exercises">
        <div className="section-heading">
          <div>
            <p className="eyebrow">03 · Required exercises</p>
            <h2>Seven complete, reproducible studies.</h2>
          </div>
          <p>
            Each exercise has code, stored data, a figure or interactive
            artifact, calculated output, interpretation, limitations, and a
            dedicated report section.
          </p>
        </div>
        <div className="exercise-list">
          {exercises.map((exercise) => (
            <a
              className="exercise-row"
              href={exercise.href}
              key={exercise.number}
              aria-label={`Open Exercise ${exercise.number}: ${exercise.title}`}
            >
              <span className="exercise-number">{exercise.number}</span>
              <div className="exercise-title">
                <div className="exercise-tags">
                  <small>{exercise.type}</small>
                  <small>{exercise.deliverable}</small>
                </div>
                <h3>{exercise.title}</h3>
              </div>
              <p>{exercise.result}</p>
              <strong className="exercise-link">Open exercise →</strong>
            </a>
          ))}
        </div>
      </section>

      <section className="section split-feature">
        <div className="feature-copy">
          <p className="eyebrow">Exercise 06 · Interactive</p>
          <h2>Color tells two different stories.</h2>
          <p>
            Use the dropdown to switch from community-like interest categories
            to a continuous popularity signal. Positions remain fixed, so color
            is the only changing visual variable.
          </p>
          <ul>
            <li>Interest group: categorical palette</li>
            <li>In-degree: continuous Viridis scale</li>
            <li>Hover: group, in-degree, and out-degree</li>
          </ul>
        </div>
        <div className="embed-frame feature-embed">
          <iframe
            title="Interactive synthetic social network color dashboard"
            src="/interactive/network_color_toggle_dashboard.html"
            loading="lazy"
          />
        </div>
      </section>

      <section className="section domain-section">
        <div className="section-heading compact">
          <div>
            <p className="eyebrow">Exercise 07 · Synthetic knowledge graph</p>
            <h2>Applied AI, methods, tools, and outcomes.</h2>
          </div>
          <p>
            Recommendation Systems has the highest inverse-strength weighted
            betweenness (0.5385), bridging research areas with methods and application
            outcomes. This is an illustrative graph, not empirical evidence.
          </p>
        </div>
        <div className="embed-frame">
          <iframe
            title="Interactive applied AI and multimedia research knowledge graph"
            src="/interactive/domain_graph.html"
            loading="lazy"
          />
        </div>
      </section>

      <section className="section method-section" id="method">
        <div className="section-heading">
          <div>
            <p className="eyebrow">04 · Method & integrity</p>
            <h2>Designed to be audited.</h2>
          </div>
          <p>
            One deterministic pipeline produces the cleaned CSV, calculated
            tables, figures, interactive HTML, notebooks, report, and site data.
          </p>
        </div>
        <div className="method-grid">
          <article>
            <span>01</span>
            <h3>Preserve</h3>
            <p>
              The official raw CSV remains unchanged. Its SHA-256 is documented,
              along with the source, DOI, license, and acquisition date.
            </p>
          </article>
          <article>
            <span>02</span>
            <h3>Transform</h3>
            <p>
              Empty columns are removed, types normalized, dates parsed, ratios
              zero-protected, and outliers flagged instead of silently deleted.
            </p>
          </article>
          <article>
            <span>03</span>
            <h3>Separate scopes</h3>
            <p>
              The real Facebook analysis stays tabular because no verified
              user relationships exist. Every relationship graph is labeled
              synthetic.
            </p>
          </article>
          <article>
            <span>04</span>
            <h3>Verify</h3>
            <p>
              Automated tests cover data invariants, graph construction,
              symmetry, weight ranges, outputs, reports, and relative paths.
            </p>
          </article>
        </div>
      </section>

      <section className="section source-section">
        <div>
          <p className="eyebrow">Dataset attribution</p>
          <h2>Facebook Live Sellers in Thailand</h2>
          <p>
            Nassim Dehouche · UCI Machine Learning Repository · DOI
            10.24432/C5R60S · Creative Commons Attribution 4.0 International.
            The official UCI archive—not the documented Kaggle mirror—was used
            because Kaggle API credentials were unavailable.
          </p>
        </div>
        <a
          className="button"
          href="https://archive.ics.uci.edu/dataset/488/facebook%2Blive%2Bsellers%2Bin%2Bthailand"
        >
          View official dataset
        </a>
      </section>

      <footer>
        <div>
          <strong>Visual Analytics & Network Analysis</strong>
          <p>
            {`© 2026 ${"S. M. Monowar Kayser"} · Daffodil International University`}
          </p>
        </div>
        <div className="footer-links">
          <a href="/report.pdf">PDF report</a>
          <a href="/report.docx">DOCX report</a>
          <a href="/report.md">Markdown report</a>
          <a href="https://github.com/Monokayser/facebook-engagement-network-visualization">
            Source repository
          </a>
        </div>
      </footer>
    </main>
  );
}
