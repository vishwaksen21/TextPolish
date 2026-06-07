import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://avelyn.software";
  const routes = [
    "",
    "/about-avelyn",
    "/what-is-avelyn",
    "/avelyn-ai",
    "/avelyn-vs-chatgpt",
    "/avelyn-vs-grammarly",
  ];

  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: "weekly",
    priority: route === "" ? 1.0 : 0.8,
  }));
}
