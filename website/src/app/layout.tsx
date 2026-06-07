import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Canonical brand metadata and search optimization config
export const metadata: Metadata = {
  metadataBase: new URL("https://avelyn.software"),
  title: {
    default: "Avelyn — Privacy-First AI Assistant for macOS",
    template: "%s | Avelyn — Privacy-First AI Assistant for macOS",
  },
  description: "Avelyn is a local offline AI writing assistant for macOS. Highlight text anywhere, trigger your global shortcut, and refine your writing system-wide with local models (Ollama) and zero cloud telemetry.",
  keywords: [
    "Avelyn", "Avelyn AI", "Avelyn Software", "Avelyn Assistant", "Avelyn Ollama", "Avelyn macOS AI Assistant",
    "offline AI assistant", "local LLM writing assistant", "privacy-first AI rewrite", "Ollama macOS client",
    "Gemma 3 mac writing app", "Llama 3 local rewrite mac"
  ],
  alternates: {
    canonical: "/",
  },
  verification: {
    google: "YuPVj-p6TNU4JjqaAoVTql78up1VAYNirhr8BYvVF3k",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-video-preview": -1,
      "max-snippet": -1,
    },
  },
  openGraph: {
    title: "Avelyn — Privacy-First AI Assistant for macOS",
    description: "Avelyn is a local offline AI writing assistant for macOS. Refine, rewrite, and perfect your text system-wide with zero cloud latency and complete privacy.",
    url: "https://avelyn.software",
    siteName: "Avelyn",
    locale: "en_US",
    type: "website",
    images: [
      {
        url: "/images/hero_image.png",
        width: 1200,
        height: 630,
        alt: "Avelyn - Local Offline AI Assistant for macOS",
      }
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Avelyn — Privacy-First AI Assistant for macOS",
    description: "Privacy-first, system-wide local offline AI writing assistant for macOS using Ollama.",
    images: ["/images/hero_image.png"],
    creator: "@vishwaksen21",
  },
  icons: {
    icon: "/logo.png",
    shortcut: "/logo.png",
    apple: "/logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Knowledge Graph structures for Organization, WebSite, and SoftwareApplication
  const orgJsonLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://avelyn.software/#organization",
    "name": "Avelyn",
    "url": "https://avelyn.software",
    "logo": "https://avelyn.software/logo.png",
    "sameAs": [
      "https://github.com/vishwaksen21/Avelyn"
    ]
  };

  const websiteJsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://avelyn.software/#website",
    "name": "Avelyn",
    "url": "https://avelyn.software",
    "publisher": {
      "@id": "https://avelyn.software/#organization"
    }
  };

  const softwareJsonLd = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "@id": "https://avelyn.software/#software",
    "name": "Avelyn",
    "alternateName": "Avelyn AI Assistant",
    "applicationCategory": "ProductivityApplication",
    "operatingSystem": "macOS",
    "downloadUrl": "https://avelyn.software/#beta",
    "url": "https://avelyn.software",
    "creator": {
      "@id": "https://avelyn.software/#organization"
    }
  };

  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-white text-neutral-900">
        {/* Brand Schema structures embedded in head/body */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(softwareJsonLd) }}
        />
        {children}
      </body>
    </html>
  );
}
