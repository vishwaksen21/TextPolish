"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Keyboard, Palette, Clock, Info, Check, ChevronDown, ChevronRight, Play } from "lucide-react";

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
    setTimeout(() => setSaveStatus("Saved"), 600);
  };

  const handleTestConnection = () => {
    setIsTesting(true);
    setIsConnected(null);
    setTimeout(() => {
      setIsTesting(false);
      setIsConnected(true);
    }, 1200);
  };

  // Ultra-premium macOS Color System
  const colors = {
    light: {
      appBg: "bg-[#FAFAFC]",
      sidebar: "bg-neutral-100/50 backdrop-blur-3xl border-r border-neutral-200/60",
      content: "bg-[#FAFAFC]",
      card: "bg-white border border-neutral-200/60 shadow-sm",
      textMain: "text-neutral-900",
      textMuted: "text-neutral-500",
      divider: "bg-neutral-100",
      input: "bg-neutral-50 border border-neutral-200/60 text-neutral-900 focus:ring-2 focus:ring-[#7C3AED]/20 focus:border-[#7C3AED]",
      navHover: "hover:bg-neutral-200/50 text-neutral-600",
      navActive: "bg-white text-neutral-900 shadow-sm border border-neutral-200/50",
    },
    dark: {
      appBg: "bg-[#1E1E1E]",
      sidebar: "bg-[#252525]/80 backdrop-blur-3xl border-r border-white/5",
      content: "bg-[#1E1E1E]",
      card: "bg-[#252525] border border-white/10 shadow-lg",
      textMain: "text-neutral-100",
      textMuted: "text-neutral-400",
      divider: "bg-white/5",
      input: "bg-[#1A1A1A] border border-white/10 text-neutral-100 focus:ring-2 focus:ring-[#7C3AED]/30 focus:border-[#7C3AED]",
      navHover: "hover:bg-white/5 text-neutral-400",
      navActive: "bg-[#333333] text-neutral-100 shadow-sm border border-white/5",
    }
  }[theme as "light" | "dark"];

  const tabs = [
    { name: "AI Provider", icon: <Sparkles className="w-4 h-4" /> },
    { name: "Hotkeys", icon: <Keyboard className="w-4 h-4" /> },
    { name: "Appearance", icon: <Palette className="w-4 h-4" /> },
    { name: "History", icon: <Clock className="w-4 h-4" /> },
    { name: "About", icon: <Info className="w-4 h-4" /> },
  ];

  // Reusable Native macOS Toggle Switch
  const Toggle = ({ checked, onChange }: { checked: boolean, onChange: (v: boolean) => void }) => (
    <button
      onClick={() => { onChange(!checked); triggerAutoSave(); }}
      className={`relative w-[38px] h-[22px] rounded-full transition-colors duration-300 ease-in-out outline-none ${checked ? "bg-[#7C3AED]" : theme === "light" ? "bg-neutral-200" : "bg-neutral-600"
        }`}
    >
      <motion.div
        layout
        className={`absolute top-[2px] left-[2px] w-[18px] h-[18px] bg-white rounded-full shadow-sm`}
        animate={{ x: checked ? 16 : 0 }}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
      />
    </button>
  );

  return (
    <section className="py-24 flex items-center justify-center relative overflow-hidden bg-[#FAFAFA]">

      {/* Ambient Presentation Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] bg-[#7C3AED]/10 blur-[120px] rounded-full pointer-events-none" />

      {/* Main App Window */}
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.98 }}
        whileInView={{ opacity: 1, y: 0, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`w-full max-w-[760px] h-[520px] ${colors.appBg} rounded-2xl shadow-2xl shadow-black/10 flex overflow-hidden relative z-10 border border-neutral-200/50 transition-colors duration-500`}
      >

        {/* SIDEBAR (Vibrancy effect) */}
        <div className={`w-[220px] ${colors.sidebar} flex flex-col pt-4 pb-4 px-3 relative z-20`}>

          {/* Traffic Lights */}
          <div className="flex gap-2 mb-8 pl-1">
            <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-black/10" />
            <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-black/10" />
            <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-black/10" />
          </div>

          {/* Search Bar */}
          <div className="mb-4">
            <div className={`w-full h-7 rounded-md ${theme === 'light' ? 'bg-neutral-200/50 text-neutral-500' : 'bg-black/20 text-neutral-400'} flex items-center px-2 text-[11px] font-medium border border-transparent`}>
              Search
            </div>
          </div>

          {/* Navigation */}
          <div className="space-y-1 flex-1">
            {tabs.map((tab) => {
              const isActive = activeTab === tab.name;
              return (
                <button
                  key={tab.name}
                  onClick={() => setActiveTab(tab.name)}
                  className={`w-full flex items-center gap-2.5 px-3 py-1.5 rounded-md text-[13px] font-medium transition-all duration-200 text-left outline-none ${isActive ? colors.navActive : colors.navHover
                    }`}
                >
                  <span className={isActive ? "text-[#7C3AED]" : ""}>{tab.icon}</span>
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </div>

          {/* Auto-Save Status */}
          <div className="flex items-center gap-2 px-2 mt-auto">
            <div className={`w-1.5 h-1.5 rounded-full ${saveStatus === "Saved" ? "bg-neutral-300" : "bg-[#7C3AED] animate-pulse"}`} />
            <span className={`text-[10px] font-semibold ${colors.textMuted}`}>{saveStatus}</span>
          </div>
        </div>

        {/* CONTENT AREA */}
        <div className={`flex-1 ${colors.content} flex flex-col relative z-10 overflow-hidden`}>
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
              className="flex-1 overflow-y-auto p-8 lg:p-10 scrollbar-none"
            >

              <h2 className={`text-2xl font-bold ${colors.textMain} tracking-tight mb-6`}>
                {activeTab}
              </h2>

              <div className="space-y-6">

                {/* --- AI PROVIDER --- */}
                {activeTab === "AI Provider" && (
                  <div className="space-y-6">
                    <div className={`${colors.card} rounded-xl overflow-hidden`}>

                      {/* Status Row */}
                      <div className="flex items-center justify-between p-4">
                        <div>
                          <div className={`text-sm font-semibold ${colors.textMain}`}>Local Engine Status</div>
                          <div className={`text-xs ${colors.textMuted} mt-0.5`}>Validate your Ollama connection</div>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${isConnected ? "bg-emerald-100 text-emerald-700" : isTesting ? "bg-amber-100 text-amber-700" : "bg-neutral-100 text-neutral-500"
                            }`}>
                            {isConnected ? "Connected" : isTesting ? "Testing..." : "Standby"}
                          </div>
                          <button
                            onClick={handleTestConnection}
                            disabled={isTesting}
                            className={`flex items-center gap-1.5 text-xs font-semibold bg-neutral-900 text-white px-3 py-1.5 rounded-lg hover:bg-neutral-800 transition-colors disabled:opacity-50`}
                          >
                            <Play className="w-3 h-3 fill-current" /> Test
                          </button>
                        </div>
                      </div>

                      <div className={`h-px w-full ${colors.divider}`} />

                      {/* Default Mode Row */}
                      <div className="flex items-center justify-between p-4">
                        <div>
                          <div className={`text-sm font-semibold ${colors.textMain}`}>Default Mode</div>
                          <div className={`text-xs ${colors.textMuted} mt-0.5`}>Primary enhancement style</div>
                        </div>
                        <select
                          value={mode}
                          onChange={(e) => { setMode(e.target.value); triggerAutoSave(); }}
                          className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-40 outline-none`}
                        >
                          <option>Professional</option>
                          <option>Fix Grammar</option>
                          <option>Concise</option>
                          <option>Explain</option>
                        </select>
                      </div>
                    </div>

                    {/* Advanced Section */}
                    <div>
                      <button
                        onClick={() => setShowAdvancedAI(!showAdvancedAI)}
                        className={`flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider ${colors.textMuted} hover:${colors.textMain} transition-colors mb-3 outline-none`}
                      >
                        {showAdvancedAI ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                        Advanced Configuration
                      </button>

                      <AnimatePresence>
                        {showAdvancedAI && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: "auto", opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            className="overflow-hidden"
                          >
                            <div className={`${colors.card} rounded-xl overflow-hidden`}>
                              <div className="flex items-center justify-between p-4">
                                <div className={`text-sm font-medium ${colors.textMain}`}>Host URL</div>
                                <input
                                  type="text"
                                  value={host}
                                  onChange={(e) => setHost(e.target.value)}
                                  onBlur={triggerAutoSave}
                                  className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-48 outline-none text-right`}
                                />
                              </div>
                              <div className={`h-px w-full ${colors.divider}`} />
                              <div className="flex items-center justify-between p-4">
                                <div className={`text-sm font-medium ${colors.textMain}`}>Default Model</div>
                                <input
                                  type="text"
                                  value={model}
                                  onChange={(e) => setModel(e.target.value)}
                                  onBlur={triggerAutoSave}
                                  className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-48 outline-none text-right`}
                                />
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                )}

                {/* --- HOTKEYS --- */}
                {activeTab === "Hotkeys" && (
                  <div className="space-y-6">
                    <div className={`${colors.card} rounded-xl overflow-hidden`}>

                      <div className="flex items-center justify-between p-4">
                        <div>
                          <div className={`text-sm font-semibold ${colors.textMain}`}>Global Shortcut</div>
                          <div className={`text-xs ${colors.textMuted} mt-0.5`}>Trigger Avelyn from anywhere</div>
                        </div>
                        <div className="flex items-center gap-2">
                          <kbd className={`px-2 py-1 rounded-md text-xs font-sans font-bold border shadow-sm ${theme === 'light' ? 'bg-white border-neutral-200 text-neutral-700' : 'bg-[#1E1E1E] border-white/10 text-neutral-300'}`}>⌘</kbd>
                          <kbd className={`px-2 py-1 rounded-md text-xs font-sans font-bold border shadow-sm ${theme === 'light' ? 'bg-white border-neutral-200 text-neutral-700' : 'bg-[#1E1E1E] border-white/10 text-neutral-300'}`}>⇧</kbd>
                          <kbd className={`px-2 py-1 rounded-md text-xs font-sans font-bold border shadow-sm ${theme === 'light' ? 'bg-white border-neutral-200 text-neutral-700' : 'bg-[#1E1E1E] border-white/10 text-neutral-300'}`}>E</kbd>
                        </div>
                      </div>

                      <div className={`h-px w-full ${colors.divider}`} />

                      <div className="flex items-center justify-between p-4">
                        <div className={`text-sm font-semibold ${colors.textMain}`}>Enable Shortcut</div>
                        <Toggle checked={hotkeyEnabled} onChange={setHotkeyEnabled} />
                      </div>

                      <div className={`h-px w-full ${colors.divider}`} />

                      <div className="flex items-center justify-between p-4">
                        <div className={`text-sm font-semibold ${colors.textMain}`}>Launch at Login</div>
                        <Toggle checked={startupEnabled} onChange={setStartupEnabled} />
                      </div>
                    </div>
                  </div>
                )}

                {/* --- APPEARANCE --- */}
                {activeTab === "Appearance" && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">

                      {/* Light Theme Button */}
                      <button
                        onClick={() => { setTheme("light"); triggerAutoSave(); }}
                        className={`flex flex-col items-center gap-3 p-4 rounded-xl border-2 transition-all duration-200 outline-none ${theme === "light" ? "border-[#7C3AED] bg-[#7C3AED]/5" : "border-transparent bg-white shadow-sm hover:border-neutral-200"
                          }`}
                      >
                        <div className="w-24 h-16 bg-[#F5F5F7] rounded-lg border border-neutral-200 overflow-hidden flex shadow-inner">
                          <div className="w-6 h-full bg-[#E8E8ED] border-r border-neutral-200"></div>
                          <div className="flex-1 p-2 space-y-1">
                            <div className="w-8 h-1.5 bg-neutral-300 rounded-full"></div>
                            <div className="w-12 h-1.5 bg-neutral-200 rounded-full"></div>
                          </div>
                        </div>
                        <span className={`text-sm font-bold ${theme === "light" ? "text-[#7C3AED]" : "text-neutral-500"}`}>Light</span>
                      </button>

                      {/* Dark Theme Button */}
                      <button
                        onClick={() => { setTheme("dark"); triggerAutoSave(); }}
                        className={`flex flex-col items-center gap-3 p-4 rounded-xl border-2 transition-all duration-200 outline-none ${theme === "dark" ? "border-[#7C3AED] bg-[#7C3AED]/5" : "border-transparent bg-[#252525] shadow-sm hover:border-neutral-600"
                          }`}
                      >
                        <div className="w-24 h-16 bg-[#1C1C1E] rounded-lg border border-neutral-700 overflow-hidden flex shadow-inner">
                          <div className="w-6 h-full bg-[#2C2C2E] border-r border-neutral-700"></div>
                          <div className="flex-1 p-2 space-y-1">
                            <div className="w-8 h-1.5 bg-neutral-600 rounded-full"></div>
                            <div className="w-12 h-1.5 bg-neutral-700 rounded-full"></div>
                          </div>
                        </div>
                        <span className={`text-sm font-bold ${theme === "dark" ? "text-[#7C3AED]" : "text-neutral-400"}`}>Dark</span>
                      </button>

                    </div>

                    <div className={`${colors.card} rounded-xl overflow-hidden mt-6`}>
                      <div className="flex items-center justify-between p-4">
                        <div className={`text-sm font-semibold ${colors.textMain}`}>System Notifications</div>
                        <Toggle checked={notifEnabled} onChange={setNotifEnabled} />
                      </div>
                    </div>
                  </div>
                )}

                {/* --- HISTORY --- */}
                {activeTab === "History" && (
                  <div className="flex flex-col items-center justify-center h-[250px] space-y-4">
                    <div className="w-16 h-16 rounded-full bg-neutral-100 flex items-center justify-center border border-neutral-200">
                      <Clock className="w-6 h-6 text-neutral-400" />
                    </div>
                    <div className="text-center">
                      <div className={`text-base font-bold ${colors.textMain}`}>No History</div>
                      <div className={`text-sm ${colors.textMuted} mt-1`}>Enhancements will appear here.</div>
                    </div>
                  </div>
                )}

                {/* --- ABOUT --- */}
                {activeTab === "About" && (
                  <div className="flex flex-col items-center justify-center h-[250px] space-y-6 text-center">
                    <img src="/logo.png" alt="Avelyn" className="w-16 h-16 drop-shadow-lg" />
                    <div>
                      <h3 className={`text-xl font-bold ${colors.textMain} tracking-tight`}>Avelyn</h3>
                      <span className={`text-xs font-semibold ${colors.textMuted} px-2 py-0.5 rounded-md bg-neutral-100 mt-1 inline-block`}>Version 1.0.0</span>
                    </div>
                    <p className={`text-sm ${colors.textMuted} max-w-[300px] leading-relaxed`}>
                      The intelligent, offline writing assistant built natively for macOS.
                    </p>
                  </div>
                )}

              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </motion.div>
    </section>
  );
}