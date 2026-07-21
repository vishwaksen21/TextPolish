import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Theme & Appearance Guide — Avelyn Documentation",
  description: "Customize dark mode, light mode, and glassmorphic UI themes.",
  alternates: { canonical: "https://avelyn.software/docs/settings/theme-appearance" },
};

export default function ThemeAppearanceDoc() {
  return (
    <DocPageLayout
      categoryTitle="Settings & Configuration"
      categorySlug="settings"
      itemSlug="theme-appearance"
      title="Theme & Appearance Customization"
      description="Customize Dark, Light, and Glassmorphic interface themes."
    >
      <h2>UI Aesthetics</h2>
      <p>Toggle between Dark, Light, and System themes in Settings → Appearance.</p>
    </DocPageLayout>
  );
}
