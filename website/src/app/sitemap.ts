import { MetadataRoute } from "next";
import { getFlatDocList } from "@/data/docsNavigation";
import { comparisonsData } from "@/data/comparisonsData";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://avelyn.software";
  const now = new Date();

  const staticRoutes = [
    "",
    "/docs",
    "/features",
    "/compare",
    "/faq",
    "/about-avelyn",
    "/what-is-avelyn",
    "/avelyn-ai",
    "/features/prompt-enhancer",
    "/features/grammar-checker",
    "/features/email-writer",
    "/features/ai-rewriter",
    "/features/ai-summarizer",
    "/features/translation",
    "/features/coding-assistant",
    "/features/ai-writing-assistant",
    "/features/mac-ai-assistant",
    "/features/local-ai",
    "/features/cloud-ai",
    "/solutions/ai-writing-assistant-mac",
    "/solutions/offline-ai-writing-assistant",
    "/solutions/prompt-enhancer-tool",
    "/solutions/grammar-correction-ai",
    "/solutions/ai-email-writer-mac",
    "/solutions/ai-productivity-app-mac",
    "/solutions/best-ai-assistant-developers",
    "/trust/about",
    "/trust/privacy",
    "/trust/terms",
    "/trust/security",
    "/trust/roadmap",
    "/trust/release-notes",
    "/trust/contact",
    "/trust/media-kit",
    "/trust/brand",
  ];

  const docsRoutes = getFlatDocList().map(
    (d) => `/docs/${d.categorySlug}/${d.item.slug}`
  );

  const compareRoutes = Object.values(comparisonsData).map(
    (c) => `/compare/${c.slug}`
  );

  const allRoutes = Array.from(
    new Set([...staticRoutes, ...docsRoutes, ...compareRoutes])
  );

  return allRoutes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: now,
    changeFrequency: route === "" ? "daily" : "weekly",
    priority: route === "" ? 1.0 : route.startsWith("/docs") ? 0.9 : 0.8,
  }));
}
