const services = [
  {
    slug: "seo-geo-audit",
    name: "SEO / GEO Audit Agent",
    category: "Digital Marketing",
    capability: "SEO Audit",
    providers: ["OpenAI", "Browser", "Google Ads"],
    level: "L4",
    risk: "medium",
    brief: ["website_url", "target_market", "target_keywords", "competitors", "cms", "business_goal"],
  },
  {
    slug: "blog-article-writer",
    name: "Blog & Article Writer",
    category: "Writing & Translation",
    capability: "Text Generation",
    providers: ["OpenAI", "Browser"],
    level: "L5",
    risk: "low",
    brief: ["topic", "audience", "tone", "target_length", "keywords", "source_links", "brand_voice"],
  },
  {
    slug: "resume-linkedin-profile",
    name: "Resume / LinkedIn Profile",
    category: "Writing & Translation",
    capability: "Career Writing",
    providers: ["OpenAI"],
    level: "L5",
    risk: "low",
    brief: ["current_resume", "target_roles", "career_level", "achievements", "constraints", "preferred_format"],
  },
  {
    slug: "translation-localization",
    name: "Translation & Localization",
    category: "Writing & Translation",
    capability: "Translation",
    providers: ["OpenAI"],
    level: "L5",
    risk: "low",
    brief: ["source_text", "source_language", "target_language", "locale", "tone", "glossary", "do_not_translate_terms"],
  },
  {
    slug: "social-media-calendar",
    name: "Social Media Calendar",
    category: "Digital Marketing",
    capability: "Content Calendar",
    providers: ["OpenAI", "Banana", "GPT Image 2"],
    level: "L4",
    risk: "medium",
    brief: ["brand", "channels", "posting_frequency", "campaign_goal", "audience", "offer", "brand_assets"],
  },
  {
    slug: "email-marketing-copy",
    name: "Email Marketing Copy",
    category: "Digital Marketing",
    capability: "Copywriting",
    providers: ["OpenAI"],
    level: "L4",
    risk: "medium",
    brief: ["audience", "offer", "funnel_stage", "brand_voice", "compliance_constraints", "cta"],
  },
  {
    slug: "landing-page-copy-wireframe",
    name: "Landing Page Copy + Wireframe",
    category: "Writing & Translation",
    capability: "Landing Page",
    providers: ["OpenAI", "GPT Image 2", "Vercel"],
    level: "L4",
    risk: "medium",
    brief: ["product", "audience", "offer", "proof_points", "competitors", "brand_assets", "conversion_goal"],
  },
  {
    slug: "presentation-pitch-deck",
    name: "Presentation / Pitch Deck",
    category: "Business",
    capability: "Presentation",
    providers: ["OpenAI", "GPT Image 2"],
    level: "L4",
    risk: "medium",
    brief: ["deck_goal", "audience", "source_materials", "brand_assets", "slide_count", "format"],
  },
  {
    slug: "market-research-brief",
    name: "Market Research Brief",
    category: "Business",
    capability: "Research",
    providers: ["OpenAI", "Browser"],
    level: "L4",
    risk: "medium",
    brief: ["market", "region", "customer_segment", "questions", "competitors", "time_horizon"],
  },
  {
    slug: "data-cleaning-formatting",
    name: "Data Cleaning & Formatting",
    category: "Data",
    capability: "Data Cleaning",
    providers: ["OpenAI"],
    level: "L5",
    risk: "low",
    brief: ["dataset_file", "target_schema", "dedupe_rules", "missing_value_rules", "output_format"],
  },
  {
    slug: "data-scraping-enrichment",
    name: "Data Scraping + Enrichment",
    category: "Data",
    capability: "Scraping",
    providers: ["OpenAI", "Browser"],
    level: "L3",
    risk: "medium",
    brief: ["target_sources", "fields", "volume", "refresh_frequency", "allowed_methods", "compliance_constraints"],
  },
  {
    slug: "dashboard-prototype",
    name: "Dashboard Prototype",
    category: "Data",
    capability: "Dashboard",
    providers: ["OpenAI"],
    level: "L4",
    risk: "low",
    brief: ["data_source", "audience", "key_metrics", "filters", "refresh_needs", "tool_preference"],
  },
  {
    slug: "website-bug-fix",
    name: "Website Bug Fix",
    category: "Programming & Tech",
    capability: "Code Fix",
    providers: ["OpenAI", "GitHub", "Vercel"],
    level: "L3",
    risk: "medium",
    brief: ["repo_url", "bug_description", "repro_steps", "expected_behavior", "environment", "access_scope"],
  },
  {
    slug: "wordpress-shopify-small-task",
    name: "WordPress / Shopify Small Task",
    category: "Programming & Tech",
    capability: "CMS Task",
    providers: ["OpenAI", "WordPress", "Shopify"],
    level: "L3",
    risk: "medium",
    brief: ["platform", "store_url", "task_description", "theme_or_plugin", "access_scope", "rollback_preference"],
  },
  {
    slug: "api-integration-automation",
    name: "API Integration / Automation",
    category: "Programming & Tech",
    capability: "Automation",
    providers: ["OpenAI", "GitHub"],
    level: "L3",
    risk: "medium",
    brief: ["systems", "trigger", "actions", "auth_method", "data_mapping", "error_handling"],
  },
  {
    slug: "ai-chatbot-agent-builder",
    name: "AI Chatbot / AI Agent Builder",
    category: "AI Services",
    capability: "AI Agent",
    providers: ["OpenAI", "GitHub"],
    level: "L3",
    risk: "medium",
    brief: ["use_case", "users", "knowledge_sources", "tools", "success_criteria", "deployment_target"],
  },
  {
    slug: "logo-concept-brand-kit",
    name: "Logo Concept / Brand Kit",
    category: "Graphics & Design",
    capability: "Brand Design",
    providers: ["OpenAI", "Banana", "GPT Image 2"],
    level: "L4",
    risk: "medium",
    brief: ["brand_name", "industry", "audience", "style_references", "colors", "usage_context", "avoid_list"],
  },
  {
    slug: "product-image-editing",
    name: "Product Image Editing",
    category: "Graphics & Design",
    capability: "Image Editing",
    providers: ["OpenAI", "Banana", "GPT Image 2"],
    level: "L4",
    risk: "medium",
    brief: ["source_images", "edit_goals", "background_style", "dimensions", "marketplace_requirements", "reference_images"],
  },
  {
    slug: "video-caption-repurpose",
    name: "Video Caption + Repurpose",
    category: "Video & Animation",
    capability: "Video Generation",
    providers: ["OpenAI", "Seedance", "Kling", "Renoise", "ElevenLabs"],
    level: "L4",
    risk: "medium",
    brief: ["source_video", "target_channels", "clip_count", "aspect_ratios", "caption_style", "music_or_voiceover_needs"],
  },
  {
    slug: "podcast-show-notes-audio-cleanup",
    name: "Podcast Notes + Audio Cleanup",
    category: "Music & Audio",
    capability: "Audio",
    providers: ["OpenAI", "ElevenLabs", "Suno"],
    level: "L4",
    risk: "medium",
    brief: ["source_audio", "episode_topic", "speaker_names", "target_platforms", "cleanup_goals", "music_needs"],
  },
];

const categoryIcons = {
  "Digital Marketing": "⌁",
  "Writing & Translation": "✎",
  Business: "▤",
  Data: "▥",
  "Programming & Tech": "<>",
  "AI Services": "✦",
  "Graphics & Design": "▧",
  "Video & Animation": "▣",
  "Music & Audio": "♪",
};

const levelMultiplier = { L1: 1.2, L2: 2, L3: 1.5, L4: 1.25, L5: 1 };
const packageBase = {
  basic: { price: 75, sla: 48 },
  standard: { price: 150, sla: 24 },
  premium: { price: 300, sla: 12 },
};

let selected = services.find((item) => item.slug === "video-caption-repurpose") || services[0];
let activeCategory = "all";
let selectedPackage = "standard";
const briefValues = new Map();

const rowsEl = document.getElementById("serviceRows");
const categoryNav = document.getElementById("categoryNav");
const categoryFilter = document.getElementById("categoryFilter");
const capabilityFilter = document.getElementById("capabilityFilter");
const providerFilter = document.getElementById("providerFilter");
const visibleCount = document.getElementById("visibleCount");
const tableSearch = document.getElementById("tableSearch");
const searchInput = document.getElementById("searchInput");

function priceFor(service, packageName = selectedPackage) {
  return Math.round(packageBase[packageName].price * levelMultiplier[service.level]);
}

function slaFor(packageName = selectedPackage) {
  return packageBase[packageName].sla;
}

function formatMoney(value) {
  return `$${value.toFixed(2)}`;
}

function titleize(field) {
  return field.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function categories() {
  return [...new Set(services.map((service) => service.category))].sort();
}

function capabilities() {
  return [...new Set(services.map((service) => service.capability))].sort();
}

function providers() {
  return [...new Set(services.flatMap((service) => service.providers))].sort();
}

function populateFilters() {
  categories().forEach((category) => {
    const count = services.filter((service) => service.category === category).length;
    const button = document.createElement("button");
    button.className = "nav-item";
    button.dataset.category = category;
    button.innerHTML = `<span class="nav-icon">${categoryIcons[category] || "•"}</span><span>${category}</span><strong>${count}</strong>`;
    button.addEventListener("click", () => {
      activeCategory = category;
      categoryFilter.value = category;
      renderAll();
    });
    categoryNav.appendChild(button);

    categoryFilter.add(new Option(`Category: ${category}`, category));
  });

  capabilities().forEach((capability) => capabilityFilter.add(new Option(`Capability: ${capability}`, capability)));
  providers().forEach((provider) => providerFilter.add(new Option(`Provider: ${provider}`, provider)));
}

function filteredServices() {
  const query = `${tableSearch.value} ${searchInput.value}`.toLowerCase().trim();
  const category = categoryFilter.value === "all" ? activeCategory : categoryFilter.value;
  const capability = capabilityFilter.value;
  const provider = providerFilter.value;
  const sort = document.getElementById("sortSelect").value;

  const result = services
    .filter((service) => category === "all" || service.category === category)
    .filter((service) => capability === "all" || service.capability === capability)
    .filter((service) => provider === "all" || service.providers.includes(provider))
    .filter((service) => {
      if (!query) return true;
      return [service.name, service.category, service.capability, service.providers.join(" ")]
        .join(" ")
        .toLowerCase()
        .includes(query);
    });

  if (sort === "price") result.sort((a, b) => priceFor(a, "basic") - priceFor(b, "basic"));
  if (sort === "sla") result.sort((a, b) => slaFor("basic") - slaFor("basic") || a.name.localeCompare(b.name));
  if (sort === "popular") result.sort((a, b) => a.name.localeCompare(b.name));
  return result;
}

function renderRows() {
  const result = filteredServices();
  rowsEl.innerHTML = "";
  visibleCount.textContent = `(${result.length})`;
  result.forEach((service, index) => {
    const row = document.createElement("tr");
    row.className = service.slug === selected.slug ? "selected" : "";
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>
        <div class="agent-cell">
          <span class="agent-mark">${categoryIcons[service.category] || "✦"}</span>
          <span class="agent-copy"><strong>${service.name}</strong><small>${service.slug}</small></span>
        </div>
      </td>
      <td>${service.category}</td>
      <td>${service.capability}</td>
      <td><div class="provider-chips">${service.providers.map((provider) => `<span class="chip">${provider}</span>`).join("")}</div></td>
      <td>$${priceFor(service, "basic")}</td>
      <td>${slaFor("basic")}h</td>
    `;
    row.addEventListener("click", () => {
      selected = service;
      renderAll();
    });
    rowsEl.appendChild(row);
  });
}

function briefKey(field) {
  return `${selected.slug}:${field}`;
}

function renderBrief() {
  const fields = document.getElementById("briefFields");
  fields.innerHTML = "";
  selected.brief.forEach((field) => {
    const row = document.createElement("div");
    row.className = "brief-row";
    const input = document.createElement("input");
    input.value = briefValues.get(briefKey(field)) || "";
    input.placeholder = `Enter ${titleize(field).toLowerCase()}`;
    input.className = input.value ? "" : "missing";
    input.addEventListener("input", () => {
      briefValues.set(briefKey(field), input.value);
      renderQuote();
    });
    row.innerHTML = `<label>${titleize(field)}</label>`;
    row.appendChild(input);
    fields.appendChild(row);
  });
}

function renderQuote() {
  document.querySelectorAll(".package-row").forEach((row) => {
    row.classList.toggle("active", row.querySelector("input").value === selectedPackage);
  });
  ["basic", "standard", "premium"].forEach((packageName) => {
    document.getElementById(`${packageName}Price`).textContent = `$${priceFor(selected, packageName)}`;
  });

  const price = priceFor(selected);
  const fee = price * 0.05;
  const escrow = price + fee;
  const complete = selected.brief.every((field) => (briefValues.get(briefKey(field)) || "").trim());

  document.getElementById("summaryPackage").textContent = selectedPackage[0].toUpperCase() + selectedPackage.slice(1);
  document.getElementById("platformFee").textContent = formatMoney(fee);
  document.getElementById("escrowHold").textContent = formatMoney(escrow);
  document.getElementById("summarySla").textContent = `${slaFor()}h`;
  document.getElementById("checkoutPrice").textContent = formatMoney(escrow);
  document.getElementById("checkoutBtn").disabled = !complete;
}

function renderWorkroom() {
  document.getElementById("selectedIcon").textContent = categoryIcons[selected.category] || "✦";
  document.getElementById("selectedName").textContent = selected.name;
  document.getElementById("selectedSub").textContent = `${selected.capability} · ${selected.category}`;
  renderBrief();
  renderQuote();
  renderProviders();
}

function renderProviders() {
  const list = document.getElementById("providerList");
  list.innerHTML = "";
  providers().forEach((provider) => {
    const needed = selected.providers.includes(provider);
    const configured = ["OpenAI", "Browser"].includes(provider);
    const row = document.createElement("div");
    row.className = "provider-row";
    row.innerHTML = `
      <span>${provider}</span>
      <small>${needed ? "Required" : "Available"}</small>
      <span class="status ${needed && !configured ? "warn" : "ok"}">${needed && !configured ? "DRY" : "OK"}</span>
    `;
    list.appendChild(row);
  });
}

function renderNav() {
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.category === activeCategory);
  });
  document.getElementById("allCount").textContent = services.length;
}

function renderAll() {
  renderNav();
  renderRows();
  renderWorkroom();
}

document.querySelector('[data-category="all"]').addEventListener("click", () => {
  activeCategory = "all";
  categoryFilter.value = "all";
  renderAll();
});

[tableSearch, searchInput, categoryFilter, capabilityFilter, providerFilter, document.getElementById("sortSelect")].forEach((control) => {
  control.addEventListener("input", renderRows);
  control.addEventListener("change", renderRows);
});

document.querySelectorAll('input[name="package"]').forEach((input) => {
  input.addEventListener("change", () => {
    selectedPackage = input.value;
    renderQuote();
  });
});

document.getElementById("autofillBrief").addEventListener("click", () => {
  selected.brief.forEach((field) => {
    briefValues.set(briefKey(field), `${titleize(field)} sample for ${selected.name}`);
  });
  renderWorkroom();
});

document.getElementById("clearSelection").addEventListener("click", () => {
  selected = services[0];
  renderAll();
});

document.getElementById("checkoutBtn").addEventListener("click", () => {
  document.getElementById("checkoutBtn").textContent = "Escrow hold created";
  setTimeout(renderQuote, 1200);
});

populateFilters();
renderAll();

