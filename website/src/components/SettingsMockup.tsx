"use client";

import React, { useState } from "react";

export default function SettingsMockup() {
  const [activeTab, setActiveTab] = useState("AI Provider");
  const [theme, setTheme] = useState("light"); // "light" | "dark"
  const [model, setModel] = useState("gemma3:4b");
  const [host, setHost] = useState("http://localhost:11434");
  const [mode, setMode] = useState("Professional");
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [isTesting, setIsTesting] = useState(false);
  const [showAdvancedAI, setShowAdvancedAI] = useState(false);
  const [showAdvancedHotkey, setShowAdvancedHotkey] = useState(false);
  const [hotkeyEnabled, setHotkeyEnabled] = useState(true);
  const [startupEnabled, setStartupEnabled] = useState(false);
  const [notifEnabled, setNotifEnabled] = useState(true);
  const [hotkey, setHotkey] = useState("Ctrl+Shift+E");
  const [rawHotkey, setRawHotkey] = useState("<ctrl>+<shift>+e");
  const [saveStatus, setSaveStatus] = useState("Saved");

  const triggerAutoSave = () => {
    setSaveStatus("Saving...");
    setTimeout(() => {
      setSaveStatus("Saved");
    }, 400);
  };

  const handleTestConnection = () => {
    setIsTesting(true);
    setIsConnected(null);
    setTimeout(() => {
      setIsTesting(false);
      setIsConnected(true);
    }, 1000);
  };

  // Color systems
  const colors = {
    light: {
      windowBg: "bg-[#F6F6F7]",
      sidebarBg: "bg-[#F6F6F7]",
      contentBg: "bg-[#F6F6F7]",
      cardBg: "bg-white",
      border: "border-[#E5E7EB]",
      textPrimary: "text-[#111827]",
      textMuted: "text-[#6B7280]",
      divider: "bg-[#E5E7EB]",
      inputBg: "bg-white",
      comboBg: "bg-white",
      navHover: "hover:bg-neutral-900/5",
      navSelected: "bg-neutral-900/5 text-[#111827] font-semibold",
      navText: "text-[#4B5563]"
    },
    dark: {
      windowBg: "bg-[#1C1C1E]",
      sidebarBg: "bg-[#1C1C1E]",
      contentBg: "bg-[#1C1C1E]",
      cardBg: "bg-[#2C2C2E]",
      border: "border-[#3C3C3E]",
      textPrimary: "text-[#F0F0F8]",
      textMuted: "text-[#9090A8]",
      divider: "bg-[#3C3C3E]",
      inputBg: "bg-[#1C1C1E]",
      comboBg: "bg-[#1C1C1E]",
      navHover: "hover:bg-white/5",
      navSelected: "bg-white/6 text-[#F0F0F8] font-semibold",
      navText: "text-[#9090A8]"
    }
  }[theme as "light" | "dark"];

  // Custom Lucide SVG Icons
  const icons = {
    sparkles: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 21L8.188 15.904L3 15L8.188 14.096L9 9L9.813 14.096L15 15L9.813 15.904Z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.071 4.929a10 10 0 00-14.142 0" />
      </svg>
    ),
    keyboard: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
        <rect x="2" y="4" width="20" height="16" rx="3" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M6 8h.01M10 8h.01M14 8h.01M18 8h.01M6 12h.01M10 12h.01M14 12h.01M18 12h.01M7 16h10" />
      </svg>
    ),
    palette: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" />
        <circle cx="7.5" cy="10.5" r="1" />
        <circle cx="11.5" cy="7.5" r="1" />
        <circle cx="16.5" cy="9.5" r="1" />
        <circle cx="15.5" cy="14.5" r="1" />
      </svg>
    ),
    clock: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
    ),
    info: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="16" x2="12" y2="12" />
        <line x1="12" y1="8" x2="12.01" y2="8" />
      </svg>
    )
  };

  const tabs = [
    { name: "AI Provider", icon: icons.sparkles },
    { name: "Hotkeys", icon: icons.keyboard },
    { name: "Appearance", icon: icons.palette },
    { name: "History", icon: icons.clock },
    { name: "About", icon: icons.info },
  ];

  return (
    <div className={`w-full max-w-[620px] ${colors.windowBg} rounded-2xl border ${colors.border} shadow-[0_24px_60px_-15px_rgba(0,0,0,0.15)] overflow-hidden font-sans select-none text-left transition-all duration-300`}>
      {/* Titlebar */}
      <div className={`h-11 ${colors.cardBg} border-b ${colors.border} flex items-center px-4 relative transition-all duration-300`}>
        <div className="flex gap-1.5 z-10">
          <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-neutral-400/20"></div>
          <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-neutral-400/20"></div>
          <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-neutral-400/20"></div>
        </div>
        <div className={`absolute inset-0 flex items-center justify-center text-xs font-semibold ${colors.textPrimary}`}>
          Avelyn — Settings
        </div>
      </div>

      <div className="flex h-[420px]">
        {/* Sidebar */}
        <div className={`w-[135px] ${colors.sidebarBg} border-r ${colors.border} flex flex-col p-3 justify-between transition-all duration-300`}>
          <div className="space-y-4">
            {/* Compact Brand Title */}
            <div className="flex items-center gap-2 px-1 py-0.5">
              <img src="/logo.png" alt="Avelyn" className="h-[18px] w-auto" />
              <span className={`font-bold text-[13px] ${colors.textPrimary} tracking-tight`}>Avelyn</span>
            </div>

            {/* Subtle borderless Navigation List */}
            <div className="space-y-0.5">
              {tabs.map((tab) => {
                const isActive = activeTab === tab.name;
                return (
                  <button
                    key={tab.name}
                    onClick={() => setActiveTab(tab.name)}
                    className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 text-left ${
                      isActive ? colors.navSelected : `${colors.navText} ${colors.navHover} hover:${colors.textPrimary}`
                    }`}
                  >
                    <span className="opacity-90">{tab.icon}</span>
                    <span>{tab.name}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Auto Save Status Indicator */}
          <div className="flex items-center gap-1.5 px-2 py-1">
            <span className={`w-1.5 h-1.5 rounded-full ${saveStatus === "Saved" ? "bg-emerald-500" : "bg-amber-500 animate-pulse"}`}></span>
            <span className="text-[10px] text-[#6B7280] font-medium">{saveStatus}</span>
          </div>
        </div>

        {/* Content Pane */}
        <div className={`flex-1 p-5 overflow-y-auto ${colors.contentBg} flex flex-col justify-between transition-all duration-300`}>
          <div className="space-y-4 w-full">
            {/* ───── AI PROVIDER PAGE ───── */}
            {activeTab === "AI Provider" && (
              <div className="space-y-4">
                <h2 className={`text-[15px] font-bold ${colors.textPrimary}`}>AI Provider</h2>
                
                {/* Basic white rounded container group */}
                <div className={`rounded-xl border ${colors.border} ${colors.cardBg} shadow-[0_1px_2px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-300`}>
                  {/* Row 1: Connection Status */}
                  <div className="flex items-center justify-between p-3.5 px-4">
                    <div className="flex flex-col gap-0.5">
                      <span className={`text-[12.5px] font-semibold ${colors.textPrimary}`}>Connection Status</span>
                      <span className={`text-[11px] ${colors.textMuted}`}>Validate local Ollama backend.</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-1.5">
                        <span className={`w-2 h-2 rounded-full ${isConnected ? "bg-emerald-500" : isTesting ? "bg-amber-500" : "bg-neutral-400"}`}></span>
                        <span className={`text-[11px] font-medium ${colors.textMuted}`}>
                          {isConnected ? "Connected" : isTesting ? "Testing..." : "Not Tested"}
                        </span>
                      </div>
                      <button
                        onClick={handleTestConnection}
                        disabled={isTesting}
                        className={`text-[11px] font-semibold ${colors.textPrimary} bg-white dark:bg-[#2C2C2E] border ${colors.border} rounded-md px-3 py-1.5 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-all cursor-pointer`}
                      >
                        Test
                      </button>
                    </div>
                  </div>
                  
                  <div className={`h-[1px] ${colors.divider}`}></div>

                  {/* Row 2: Default Writing Mode */}
                  <div className="flex items-center justify-between p-3.5 px-4">
                    <div className="flex flex-col gap-0.5">
                      <span className={`text-[12.5px] font-semibold ${colors.textPrimary}`}>Default Mode</span>
                      <span className={`text-[11px] ${colors.textMuted}`}>Primary preset for text enhancement.</span>
                    </div>
                    <select
                      value={mode}
                      onChange={(e) => {
                        setMode(e.target.value);
                        triggerAutoSave();
                      }}
                      className={`text-xs ${colors.inputBg} border ${colors.border} ${colors.textPrimary} rounded-md px-2 py-1 focus:outline-none focus:border-[#7C3AED] transition-colors cursor-pointer w-[140px] font-medium`}
                    >
                      <option>Professional</option>
                      <option>Fix Grammar</option>
                      <option>Shorten</option>
                      <option>Explain Code</option>
                    </select>
                  </div>
                </div>

                {/* Advanced expandable section */}
                <button
                  onClick={() => setShowAdvancedAI(!showAdvancedAI)}
                  className={`text-xs font-semibold ${colors.textMuted} hover:${colors.textPrimary} flex items-center gap-1 px-1 py-0.5 cursor-pointer`}
                >
                  <span className="text-[10px]">{showAdvancedAI ? "▼" : "▶"}</span>
                  <span>Advanced Settings</span>
                </button>

                {showAdvancedAI && (
                  <div className={`rounded-xl border ${colors.border} ${colors.cardBg} shadow-[0_1px_2px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-300`}>
                    <div className="flex items-center justify-between p-3 px-4">
                      <span className={`text-[12px] font-semibold ${colors.textPrimary}`}>Provider Type</span>
                      <span className={`text-xs font-semibold ${colors.textMuted}`}>Ollama (Local)</span>
                    </div>
                    <div className={`h-[1px] ${colors.divider}`}></div>
                    
                    <div className="flex items-center justify-between p-3 px-4">
                      <span className={`text-[12px] font-semibold ${colors.textPrimary}`}>Ollama API Host</span>
                      <input
                        type="text"
                        value={host}
                        onChange={(e) => setHost(e.target.value)}
                        onBlur={triggerAutoSave}
                        className={`text-xs ${colors.inputBg} border ${colors.border} ${colors.textPrimary} rounded-md px-2.5 py-1.5 w-44 focus:outline-none focus:border-[#7C3AED] text-right font-medium`}
                      />
                    </div>
                    <div className={`h-[1px] ${colors.divider}`}></div>

                    <div className="flex items-center justify-between p-3 px-4">
                      <span className={`text-[12px] font-semibold ${colors.textPrimary}`}>AI Model ID</span>
                      <input
                        type="text"
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                        onBlur={triggerAutoSave}
                        className={`text-xs ${colors.inputBg} border ${colors.border} ${colors.textPrimary} rounded-md px-2.5 py-1.5 w-44 focus:outline-none focus:border-[#7C3AED] text-right font-medium`}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* ───── HOTKEYS PAGE ───── */}
            {activeTab === "Hotkeys" && (
              <div className="space-y-4">
                <h2 className={`text-[15px] font-bold ${colors.textPrimary}`}>Hotkeys</h2>
                
                <div className={`rounded-xl border ${colors.border} ${colors.cardBg} shadow-[0_1px_2px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-300`}>
                  {/* Row 1: Global Shortcut displaying beautiful caps */}
                  <div className="flex items-center justify-between p-3.5 px-4">
                    <div className="flex flex-col gap-0.5">
                      <span className={`text-[12.5px] font-semibold ${colors.textPrimary}`}>Keyboard Shortcut</span>
                      <span className={`text-[11px] ${colors.textMuted}`}>Global key combination trigger.</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <span className={`px-2 py-1 rounded border ${theme === 'light' ? 'border-[#D1D5DB] bg-white text-[#111827]' : 'border-[#4C4C4E] bg-[#1C1C1E] text-[#F0F0F8]'} text-xs font-bold shadow-sm`}>⌃</span>
                        <span className={`px-2 py-1 rounded border ${theme === 'light' ? 'border-[#D1D5DB] bg-white text-[#111827]' : 'border-[#4C4C4E] bg-[#1C1C1E] text-[#F0F0F8]'} text-xs font-bold shadow-sm`}>⇧</span>
                        <span className={`px-2 py-1 rounded border ${theme === 'light' ? 'border-[#D1D5DB] bg-white text-[#111827]' : 'border-[#4C4C4E] bg-[#1C1C1E] text-[#F0F0F8]'} text-xs font-bold shadow-sm`}>E</span>
                      </div>
                      <input
                        type="text"
                        value={hotkey}
                        onChange={(e) => setHotkey(e.target.value)}
                        onBlur={triggerAutoSave}
                        className={`text-xs ${colors.inputBg} border ${colors.border} ${colors.textPrimary} rounded-md px-2 py-1 w-24 focus:outline-none focus:border-[#7C3AED] font-medium`}
                      />
                    </div>
                  </div>
                  
                  <div className={`h-[1px] ${colors.divider}`}></div>

                  {/* Row 2: Enable Shortcut */}
                  <div className="flex items-center justify-between p-3.5 px-4">
                    <span className={`text-[12.5px] font-semibold ${colors.textPrimary}`}>Enable Shortcut</span>
                    <input
                      type="checkbox"
                      checked={hotkeyEnabled}
                      onChange={(e) => {
                        setHotkeyEnabled(e.target.checked);
                        triggerAutoSave();
                      }}
                      className="cursor-pointer accent-[#7C3AED] w-4 h-4"
                    />
                  </div>

                  <div className={`h-[1px] ${colors.divider}`}></div>

                  {/* Row 3: Launch at Login */}
                  <div className="flex items-center justify-between p-3.5 px-4">
                    <span className={`text-[12.5px] font-semibold ${colors.textPrimary}`}>Launch at Login</span>
                    <input
                      type="checkbox"
                      checked={startupEnabled}
                      onChange={(e) => {
                        setStartupEnabled(e.target.checked);
                        triggerAutoSave();
                      }}
                      className="cursor-pointer accent-[#7C3AED] w-4 h-4"
                    />
                  </div>
                </div>

                {/* Advanced Raw Hotkey details */}
                <button
                  onClick={() => setShowAdvancedHotkey(!showAdvancedHotkey)}
                  className={`text-xs font-semibold ${colors.textMuted} hover:${colors.textPrimary} flex items-center gap-1 px-1 py-0.5 cursor-pointer`}
                >
                  <span className="text-[10px]">{showAdvancedHotkey ? "▼" : "▶"}</span>
                  <span>Advanced Hotkey Details</span>
                </button>

                {showAdvancedHotkey && (
                  <div className={`rounded-xl border ${colors.border} ${colors.cardBg} shadow-[0_1px_2px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-300`}>
                    <div className="flex items-center justify-between p-3 px-4">
                      <span className={`text-[12px] font-semibold ${colors.textPrimary}`}>Raw internal mapping</span>
                      <input
                        type="text"
                        value={rawHotkey}
                        onChange={(e) => setRawHotkey(e.target.value)}
                        onBlur={triggerAutoSave}
                        className={`text-xs ${colors.inputBg} border ${colors.border} ${colors.textPrimary} rounded-md px-2 py-1.5 w-44 focus:outline-none focus:border-[#7C3AED] text-right font-medium`}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* ───── APPEARANCE PAGE ───── */}
            {activeTab === "Appearance" && (
              <div className="space-y-4">
                <h2 className={`text-[15px] font-bold ${colors.textPrimary}`}>Appearance</h2>
                
                {/* 3 side-by-side visual cards */}
                <div className={`rounded-xl border ${colors.border} ${colors.cardBg} p-4 shadow-[0_1px_2px_rgba(0,0,0,0.02)] transition-all duration-300`}>
                  <span className={`text-xs font-semibold ${colors.textMuted}`}>Theme preferences</span>
                  <div className="flex gap-4 mt-3">
                    {/* Light Card */}
                    <button
                      onClick={() => {
                        setTheme("light");
                        triggerAutoSave();
                      }}
                      className={`flex-1 flex flex-col items-center gap-2 p-2.5 rounded-lg border transition-all duration-200 cursor-pointer ${
                        theme === "light" ? "border-[#7C3AED] bg-violet-500/5 font-semibold text-[#7C3AED]" : `${colors.border} ${colors.cardBg} hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-500`
                      }`}
                    >
                      {/* Mini mockup preview window */}
                      <div className="w-[100px] h-[55px] bg-[#FFFFFF] rounded-md border border-[#E5E7EB] overflow-hidden p-1 relative flex">
                        {/* Sidebar */}
                        <div className="w-[24px] h-full bg-[#F8F8FA] border-r border-[#E5E7EB] flex flex-col gap-0.5 p-0.5">
                          <div className="w-1 h-1 rounded-full bg-[#FF5F56]"></div>
                          <div className="w-full h-1 bg-[#E5E7EB] rounded mt-1"></div>
                        </div>
                        <div className="flex-1 p-1 space-y-1">
                          <div className="w-12 h-1 bg-neutral-900 rounded"></div>
                          <div className="w-8 h-1 bg-[#6B7280] rounded"></div>
                        </div>
                      </div>
                      <span className="text-[11px]">Light Mode</span>
                    </button>

                    {/* Dark Card */}
                    <button
                      onClick={() => {
                        setTheme("dark");
                        triggerAutoSave();
                      }}
                      className={`flex-1 flex flex-col items-center gap-2 p-2.5 rounded-lg border transition-all duration-200 cursor-pointer ${
                        theme === "dark" ? "border-[#7C3AED] bg-violet-500/5 font-semibold text-[#7C3AED]" : `${colors.border} ${colors.cardBg} hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-500`
                      }`}
                    >
                      {/* Mini mockup preview window */}
                      <div className="w-[100px] h-[55px] bg-[#121216] rounded-md border border-[#222230] overflow-hidden p-1 relative flex">
                        {/* Sidebar */}
                        <div className="w-[24px] h-full bg-[#171721] border-r border-[#222230] flex flex-col gap-0.5 p-0.5">
                          <div className="w-1 h-1 rounded-full bg-[#FF5F56]"></div>
                          <div className="w-full h-1 bg-[#3C3C3E] rounded mt-1"></div>
                        </div>
                        <div className="flex-1 p-1 space-y-1">
                          <div className="w-12 h-1 bg-white rounded"></div>
                          <div className="w-8 h-1 bg-[#9090A8] rounded"></div>
                        </div>
                      </div>
                      <span className="text-[11px]">Dark Mode</span>
                    </button>

                    {/* System Card (Split preview) */}
                    <button
                      disabled
                      className="flex-1 flex flex-col items-center gap-2 p-2.5 rounded-lg border border-dashed border-neutral-300 dark:border-neutral-700 opacity-60 text-neutral-400 text-left relative"
                    >
                      {/* Split Preview */}
                      <div className="w-[100px] h-[55px] rounded-md overflow-hidden relative border border-[#E5E7EB] dark:border-[#222230] flex">
                        {/* Light Half */}
                        <div className="absolute inset-0 bg-[#FFFFFF] flex">
                          <div className="w-[24px] h-full bg-[#F8F8FA] border-r border-[#E5E7EB]"></div>
                        </div>
                        {/* Dark Half (diagonal split clip) */}
                        <div
                          className="absolute inset-0 bg-[#121216] flex"
                          style={{ clipPath: "polygon(100% 0, 100% 100%, 0 100%)" }}
                        >
                          <div className="w-[24px] h-full bg-[#171721] border-r border-[#222230]"></div>
                        </div>
                      </div>
                      <span className="text-[11px]">System (N/A)</span>
                    </button>
                  </div>
                </div>

                {/* Notifications row */}
                <div className={`rounded-xl border ${colors.border} ${colors.cardBg} shadow-[0_1px_2px_rgba(0,0,0,0.02)] overflow-hidden transition-all duration-300`}>
                  <div className="flex items-center justify-between p-3.5 px-4">
                    <span className={`text-[12.5px] font-semibold ${colors.textPrimary}`}>System Notifications</span>
                    <input
                      type="checkbox"
                      checked={notifEnabled}
                      onChange={(e) => {
                        setNotifEnabled(e.target.checked);
                        triggerAutoSave();
                      }}
                      className="cursor-pointer accent-[#7C3AED] w-4 h-4"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* ───── HISTORY PAGE ───── */}
            {activeTab === "History" && (
              <div className="space-y-4">
                <h2 className={`text-[15px] font-bold ${colors.textPrimary}`}>History</h2>
                
                {/* Centered, card-less empty state clock */}
                <div className="flex flex-col items-center justify-center py-10 space-y-3">
                  <div className="p-3 bg-violet-500/5 rounded-full border border-violet-500/10">
                    {icons.clock}
                  </div>
                  <div className="text-center space-y-1">
                    <h4 className={`text-sm font-bold ${colors.textPrimary}`}>No History Yet</h4>
                    <p className={`text-xs ${colors.textMuted} max-w-[220px]`}>
                      Enhancements you apply will appear here.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* ───── ABOUT PAGE ───── */}
            {activeTab === "About" && (
              <div className="flex flex-col items-center text-center pt-4 space-y-3 w-full">
                {/* Centered Native layout */}
                <div className="p-3 bg-white rounded-xl border border-neutral-200/50 shadow-sm">
                  <img src="/logo.png" alt="Avelyn" className="w-[36px] h-[36px]" />
                </div>
                <div className="space-y-1">
                  <h3 className={`text-base font-bold ${colors.textPrimary}`}>Avelyn</h3>
                  <span className={`text-[11px] ${colors.textMuted} font-medium`}>Version 1.0.0</span>
                </div>
                
                <p className={`text-xs ${colors.textMuted} leading-relaxed max-w-[280px]`}>
                  Avelyn is a private, lightning-fast text enhancer that runs locally on your Mac. Improve clarity, fix grammar, and polish your writing in any application.
                </p>

                {/* Simple text link row */}
                <div className="flex gap-4 pt-4 text-xs font-semibold text-[#7C3AED]">
                  <a href="https://avelyn.app" target="_blank" className="hover:underline">Website</a>
                  <span className="text-neutral-300 dark:text-neutral-700 select-none">·</span>
                  <a href="https://github.com/vishwaksen21/Avelyn" target="_blank" className="hover:underline">GitHub</a>
                  <span className="text-neutral-300 dark:text-neutral-700 select-none">·</span>
                  <a href="https://avelyn.app/privacy" target="_blank" className="hover:underline">Privacy</a>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
