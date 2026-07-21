import React from "react";
import Link from "next/link";
import { ChevronRight, Home } from "lucide-react";

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

export default function Breadcrumbs({ items }: BreadcrumbsProps) {
  return (
    <nav aria-label="Breadcrumb" className="mb-6 flex items-center space-x-2 text-sm text-neutral-500 overflow-x-auto whitespace-nowrap">
      <Link href="/" className="flex items-center hover:text-neutral-900 transition-colors">
        <Home className="w-3.5 h-3.5 mr-1" />
        <span>Home</span>
      </Link>

      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <React.Fragment key={index}>
            <ChevronRight className="w-3.5 h-3.5 text-neutral-300 flex-shrink-0" />
            {item.href && !isLast ? (
              <Link href={item.href} className="hover:text-neutral-900 transition-colors">
                {item.label}
              </Link>
            ) : (
              <span className="font-medium text-neutral-900 truncate">{item.label}</span>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
}
