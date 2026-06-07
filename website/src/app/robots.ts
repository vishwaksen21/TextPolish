import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
      },
      {
        userAgent: "GoogleBot",
        allow: "/",
      },
      {
        // Optimization for AI search crawlers
        userAgent: ["ChatGPT-User", "Claude-Web", "PerplexityBot", "Applebot-Extended"],
        allow: "/",
      }
    ],
    sitemap: "https://avelyn.software/sitemap.xml",
  };
}
