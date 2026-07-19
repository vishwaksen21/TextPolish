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
  
  const [revealHistory, setRevealHistory] = useState(false);
  const [providerMode, setProviderMode] = useState("auto"); // "single" | "smart_router" | "auto"
  const [singleProvider, setSingleProvider] = useState("ollama"); // "ollama" | "avelyn_cloud" | "custom_api"
  const [cloudApiKey, setCloudApiKey] = useState("sk-or-v1-d6c91...");
  const [cloudModel, setCloudModel] = useState("google/gemini-2.5-flash");
  const [customPreset, setCustomPreset] = useState("OpenAI");
  const [customBaseUrl, setCustomBaseUrl] = useState("https://api.openai.com/v1");
  const [customApiKey, setCustomApiKey] = useState("");
  const [customModel, setCustomModel] = useState("gpt-4o-mini");
  const [fallbackEnabled, setFallbackEnabled] = useState(true);
  const [fallbackChain, setFallbackChain] = useState("ollama, avelyn_cloud, custom_api");
  
  const [codingProvider, setCodingProvider] = useState("avelyn_cloud");
  const [codingModel, setCodingModel] = useState("moonshotai/kimi-k2:free");
  const [writingProvider, setWritingProvider] = useState("avelyn_cloud");
  const [writingModel, setWritingModel] = useState("anthropic/claude-3.5-haiku");
  const [reasoningProvider, setReasoningProvider] = useState("custom_api");
  const [reasoningModel, setReasoningModel] = useState("google/gemini-2.5-flash");

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
        className={`w-full max-w-[760px] h-[540px] sm:h-[520px] ${colors.appBg} rounded-2xl shadow-2xl shadow-black/10 flex flex-col sm:flex-row overflow-hidden relative z-10 border border-neutral-200/50 transition-colors duration-500`}
      >

        {/* SIDEBAR (Vibrancy effect) */}
        <div className={`w-full sm:w-[220px] ${colors.sidebar} flex flex-col pt-3 pb-3 sm:pt-4 sm:pb-4 px-3 relative z-20 border-b sm:border-b-0 sm:border-r border-neutral-200/60`}>

          {/* Traffic Lights */}
          <div className="hidden sm:flex gap-2 mb-8 pl-1">
            <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-black/10" />
            <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-black/10" />
            <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-black/10" />
          </div>

          {/* Search Bar */}
          <div className="hidden sm:block mb-4">
            <div className={`w-full h-7 rounded-md ${theme === 'light' ? 'bg-neutral-200/50 text-neutral-500' : 'bg-black/20 text-neutral-400'} flex items-center px-2 text-[11px] font-medium border border-transparent`}>
              Search
            </div>
          </div>

          {/* Navigation */}
          <div className="flex flex-row sm:flex-col overflow-x-auto scrollbar-none gap-1 sm:space-y-1 flex-1 w-full pb-1 sm:pb-0">
            {tabs.map((tab) => {
              const isActive = activeTab === tab.name;
              return (
                <button
                  key={tab.name}
                  onClick={() => setActiveTab(tab.name)}
                  className={`flex items-center gap-2.5 px-3 py-1.5 rounded-md text-[13px] font-medium transition-all duration-200 text-left outline-none shrink-0 ${isActive ? colors.navActive : colors.navHover
                    }`}
                >
                  <span className={isActive ? "text-[#7C3AED]" : ""}>{tab.icon}</span>
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </div>

          {/* Auto-Save Status */}
          <div className="hidden sm:flex items-center gap-2 px-2 mt-auto">
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
              className="flex-1 overflow-y-auto p-5 sm:p-8 lg:p-10 scrollbar-none"
            >

              <h2 className={`text-2xl font-bold ${colors.textMain} tracking-tight mb-6`}>
                {activeTab}
              </h2>

              <div className="space-y-6">

                {/* --- AI PROVIDER --- */}
                {activeTab === "AI Provider" && (
                  <div className="space-y-5">
                    {/* Mode Selector Segmented Control */}
                    <div className={`p-1 rounded-lg ${theme === 'light' ? 'bg-neutral-200/50' : 'bg-black/30'} flex`}>
                      {[
                        { id: "auto", label: "Auto Provider (Intelligent)" },
                        { id: "smart_router", label: "Smart Router" },
                        { id: "single", label: "Single Provider" },
                      ].map((m) => (
                        <button
                          key={m.id}
                          onClick={() => { setProviderMode(m.id); triggerAutoSave(); }}
                          className={`flex-1 text-center py-1.5 rounded-md text-[11px] font-bold transition-all duration-200 outline-none ${
                            providerMode === m.id
                              ? "bg-[#7C3AED] text-white shadow-sm"
                              : theme === 'light'
                              ? "text-neutral-600 hover:text-neutral-900"
                              : "text-neutral-400 hover:text-neutral-200"
                          }`}
                        >
                          {m.label}
                        </button>
                      ))}
                    </div>

                    {/* Auto Mode Config Panel */}
                    {providerMode === "auto" && (
                      <div className={`${colors.card} rounded-xl p-5 space-y-3`}>
                        <div className="flex items-start gap-3">
                          <div className="p-2 rounded-lg bg-[#7C3AED]/10 text-[#7C3AED] shrink-0 mt-0.5">
                            <Sparkles className="w-5 h-5" />
                          </div>
                          <div>
                            <h4 className={`text-sm font-semibold ${colors.textMain}`}>Auto Provider Mode Active</h4>
                            <p className={`text-xs ${colors.textMuted} mt-1 leading-relaxed`}>
                              Avelyn dynamically routes tasks based on privacy, length, and task classification:
                            </p>
                            <ul className={`list-disc pl-4 text-[11px] ${colors.textMuted} mt-2.5 space-y-1.5`}>
                              <li>Privacy-focused instructions are kept fully local via <strong>Ollama</strong>.</li>
                              <li>Short text queries (&lt; 50 chars) process locally for absolute privacy.</li>
                              <li>Coding scripts and syntax route automatically to the <strong>Coding Provider</strong>.</li>
                              <li>Large documents (&gt; 2,000 chars) route to the <strong>Writing Provider</strong>.</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Single Provider Panel */}
                    {providerMode === "single" && (
                      <div className="space-y-4">
                        <div className={`${colors.card} rounded-xl p-4 space-y-3`}>
                          <div className={`text-[10px] font-bold uppercase tracking-wider ${colors.textMuted}`}>Select Active Provider</div>
                          <div className="grid grid-cols-3 gap-2">
                            {[
                              { id: "ollama", label: "Local Ollama" },
                              { id: "avelyn_cloud", label: "Avelyn Cloud" },
                              { id: "custom_api", label: "Custom API" }
                            ].map((prov) => (
                              <button
                                key={prov.id}
                                onClick={() => { setSingleProvider(prov.id); triggerAutoSave(); }}
                                className={`py-1.5 px-2 text-[11px] font-bold rounded-lg border transition-all duration-200 text-center outline-none ${
                                  singleProvider === prov.id
                                    ? "border-[#7C3AED] bg-[#7C3AED]/5 text-[#7C3AED]"
                                    : theme === 'light'
                                    ? "border-neutral-200 hover:border-neutral-300 text-neutral-600 bg-neutral-50/50"
                                    : "border-white/10 hover:border-white/20 text-neutral-400 bg-white/5"
                                }`}
                              >
                                {prov.label}
                              </button>
                            ))}
                          </div>
                        </div>

                        {/* Local Ollama Card */}
                        {singleProvider === "ollama" && (
                          <div className={`${colors.card} rounded-xl overflow-hidden`}>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 border-b border-neutral-200/40">
                              <div>
                                <div className={`text-sm font-semibold ${colors.textMain}`}>Local Engine Connection</div>
                                <div className={`text-xs ${colors.textMuted} mt-0.5`}>Validate your Ollama endpoint</div>
                              </div>
                              <div className="flex items-center gap-3">
                                <div className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${isConnected ? "bg-emerald-100 text-emerald-700" : isTesting ? "bg-amber-100 text-amber-700" : "bg-neutral-100 text-neutral-500"}`}>
                                  {isConnected ? "Connected" : isTesting ? "Testing..." : "Standby"}
                                </div>
                                <button onClick={handleTestConnection} disabled={isTesting} className="flex items-center gap-1.5 text-xs font-semibold bg-neutral-900 text-white px-3 py-1.5 rounded-lg hover:bg-neutral-800 transition-colors disabled:opacity-50">
                                  <Play className="w-3 h-3 fill-current" /> Test
                                </button>
                              </div>
                            </div>
                            <div className="p-4 space-y-4">
                              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                                <div className={`text-sm font-medium ${colors.textMain}`}>Host URL</div>
                                <input type="text" value={host} onChange={(e) => setHost(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                              </div>
                              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                                <div className={`text-sm font-medium ${colors.textMain}`}>Default Model</div>
                                <input type="text" value={model} onChange={(e) => setModel(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Avelyn Cloud Card */}
                        {singleProvider === "avelyn_cloud" && (
                          <div className={`${colors.card} rounded-xl p-4 space-y-4`}>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div>
                                <div className={`text-sm font-semibold ${colors.textMain}`}>API Key</div>
                                <div className={`text-xs ${colors.textMuted} mt-0.5`}>Your OpenRouter API Key (sk-or-v1-...)</div>
                              </div>
                              <input type="password" value={cloudApiKey} onChange={(e) => setCloudApiKey(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                            </div>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div>
                                <div className={`text-sm font-semibold ${colors.textMain}`}>Preferred Model</div>
                                <div className={`text-xs ${colors.textMuted} mt-0.5`}>Select your cloud model override</div>
                              </div>
                              <select value={cloudModel} onChange={(e) => { setCloudModel(e.target.value); triggerAutoSave(); }} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none`}>
                                <option value="openai/gpt-4o-mini">GPT-4o Mini (Fast & Cheap)</option>
                                <option value="anthropic/claude-3.5-haiku">Claude 3.5 Haiku</option>
                                <option value="google/gemini-2.5-flash">Gemini 2.5 Flash (Ultra Fast)</option>
                                <option value="deepseek/deepseek-chat-v3-0324:free">DeepSeek V3 (Free)</option>
                              </select>
                            </div>
                          </div>
                        )}

                        {/* Custom API Card */}
                        {singleProvider === "custom_api" && (
                          <div className={`${colors.card} rounded-xl p-4 space-y-4`}>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div className={`text-sm font-medium ${colors.textMain}`}>Preset</div>
                              <select value={customPreset} onChange={(e) => { setCustomPreset(e.target.value); triggerAutoSave(); }} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none`}>
                                <option>OpenAI</option>
                                <option>Anthropic</option>
                                <option>LM Studio</option>
                                <option>vLLM</option>
                              </select>
                            </div>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div className={`text-sm font-medium ${colors.textMain}`}>Base URL</div>
                              <input type="text" value={customBaseUrl} onChange={(e) => setCustomBaseUrl(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                            </div>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div className={`text-sm font-medium ${colors.textMain}`}>API Key</div>
                              <input type="password" placeholder="Optional" value={customApiKey} onChange={(e) => setCustomApiKey(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                            </div>
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div className={`text-sm font-medium ${colors.textMain}`}>Model Name</div>
                              <input type="text" value={customModel} onChange={(e) => setCustomModel(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Smart Router Panel */}
                    {providerMode === "smart_router" && (
                      <div className="space-y-4">
                        <div className={`${colors.card} rounded-xl p-4 space-y-4`}>
                          <div className={`text-[10px] font-bold uppercase tracking-wider ${colors.textMuted}`}>Route Overrides per Task Group</div>
                          
                          {/* Coding task override */}
                          <div className="space-y-2 border-b border-neutral-200/40 pb-3">
                            <div className="flex justify-between items-center">
                              <span className={`text-xs font-semibold ${colors.textMain}`}>Coding Tasks</span>
                              <select value={codingProvider} onChange={(e) => { setCodingProvider(e.target.value); triggerAutoSave(); }} className={`text-[11px] font-medium ${colors.input} rounded-md px-2 py-1 outline-none`}>
                                <option value="ollama">Ollama</option>
                                <option value="avelyn_cloud">Avelyn Cloud</option>
                                <option value="custom_api">Custom API</option>
                              </select>
                            </div>
                            <input type="text" value={codingModel} onChange={(e) => setCodingModel(e.target.value)} onBlur={triggerAutoSave} className={`text-[11px] ${colors.input} rounded-md px-2 py-1 w-full outline-none`} placeholder="Model Override ID" />
                          </div>

                          {/* Writing task override */}
                          <div className="space-y-2 border-b border-neutral-200/40 pb-3">
                            <div className="flex justify-between items-center">
                              <span className={`text-xs font-semibold ${colors.textMain}`}>Writing Tasks</span>
                              <select value={writingProvider} onChange={(e) => { setWritingProvider(e.target.value); triggerAutoSave(); }} className={`text-[11px] font-medium ${colors.input} rounded-md px-2 py-1 outline-none`}>
                                <option value="ollama">Ollama</option>
                                <option value="avelyn_cloud">Avelyn Cloud</option>
                                <option value="custom_api">Custom API</option>
                              </select>
                            </div>
                            <input type="text" value={writingModel} onChange={(e) => setWritingModel(e.target.value)} onBlur={triggerAutoSave} className={`text-[11px] ${colors.input} rounded-md px-2 py-1 w-full outline-none`} placeholder="Model Override ID" />
                          </div>

                          {/* Reasoning task override */}
                          <div className="space-y-2">
                            <div className="flex justify-between items-center">
                              <span className={`text-xs font-semibold ${colors.textMain}`}>Reasoning Tasks</span>
                              <select value={reasoningProvider} onChange={(e) => { setReasoningProvider(e.target.value); triggerAutoSave(); }} className={`text-[11px] font-medium ${colors.input} rounded-md px-2 py-1 outline-none`}>
                                <option value="ollama">Ollama</option>
                                <option value="avelyn_cloud">Avelyn Cloud</option>
                                <option value="custom_api">Custom API</option>
                              </select>
                            </div>
                            <input type="text" value={reasoningModel} onChange={(e) => setReasoningModel(e.target.value)} onBlur={triggerAutoSave} className={`text-[11px] ${colors.input} rounded-md px-2 py-1 w-full outline-none`} placeholder="Model Override ID" />
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Smart Fallback & Search Chain Priority */}
                    <div className={`${colors.card} rounded-xl p-4 space-y-4`}>
                      <div className="flex items-center justify-between">
                        <div>
                          <div className={`text-sm font-semibold ${colors.textMain}`}>Smart Fallback</div>
                          <div className={`text-xs ${colors.textMuted} mt-0.5`}>Retry next provider automatically if primary fails</div>
                        </div>
                        <Toggle checked={fallbackEnabled} onChange={setFallbackEnabled} />
                      </div>
                      <div className={`h-px w-full ${colors.divider}`} />
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                          <div className={`text-sm font-semibold ${colors.textMain}`}>Fallback Search Priority</div>
                          <div className={`text-xs ${colors.textMuted} mt-0.5`}>Order of providers to search (comma-separated)</div>
                        </div>
                        <input type="text" value={fallbackChain} onChange={(e) => setFallbackChain(e.target.value)} onBlur={triggerAutoSave} className={`text-sm font-medium ${colors.input} rounded-lg px-3 py-1.5 w-full sm:w-48 outline-none text-left sm:text-right`} />
                      </div>
                    </div>
                  </div>
                )}

                {/* --- HOTKEYS --- */}
                {activeTab === "Hotkeys" && (
                  <div className="space-y-6">
                    <div className={`${colors.card} rounded-xl overflow-hidden`}>

                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4">
                        <div>
                          <div className={`text-sm font-semibold ${colors.textMain}`}>Global Shortcut</div>
                          <div className={`text-xs ${colors.textMuted} mt-0.5`}>Trigger Avelyn from anywhere</div>
                        </div>
                        <div className="flex items-center gap-2 self-start sm:self-auto">
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
                  <div className="flex flex-col items-center justify-center min-h-[250px]">
                    {!revealHistory ? (
                      <div className="flex flex-col items-center justify-center text-center space-y-4 max-w-[280px]">
                        <div className="w-12 h-12 rounded-full bg-amber-50 dark:bg-amber-950/30 flex items-center justify-center border border-amber-200 dark:border-amber-900/30 text-amber-600 dark:text-amber-400 shadow-sm animate-pulse">
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                          </svg>
                        </div>
                        <div>
                          <h4 className={`text-sm font-bold ${colors.textMain}`}>History Hidden for Privacy</h4>
                          <p className={`text-[11px] ${colors.textMuted} mt-1 leading-relaxed`}>
                            Your enhancement history is locked. Click the button below to decrypt and reveal history.
                          </p>
                        </div>
                        <button
                          onClick={() => setRevealHistory(true)}
                          className="bg-[#7C3AED] hover:bg-[#6D28D9] text-white text-[11px] font-bold py-2 px-4 rounded-lg shadow-md transition-colors"
                        >
                          Reveal History
                        </button>
                      </div>
                    ) : (
                      <div className="w-full space-y-3 px-1 max-h-[250px] overflow-y-auto scrollbar-none">
                        <div className="flex justify-between items-center mb-1">
                          <span className={`text-[10px] font-bold uppercase tracking-wider ${colors.textMuted}`}>Decrypted Prompt Logs</span>
                          <button onClick={() => setRevealHistory(false)} className="text-[10px] text-[#7C3AED] font-bold hover:underline">Lock History</button>
                        </div>
                        {[
                          { mode: "professional", date: "Just now", snippet: "Drafted professional email to engineering team" },
                          { mode: "grammar", date: "2 mins ago", snippet: "Grammar review: fixed missing punctuation in report" },
                          { mode: "explain_code", date: "15 mins ago", snippet: "Explained python decorator class implementation" }
                        ].map((h, idx) => (
                          <div key={idx} className={`${colors.card} p-3 rounded-lg flex items-center justify-between text-left`}>
                            <div className="space-y-1">
                              <div className={`text-[11px] font-semibold ${colors.textMain}`}>{h.snippet}</div>
                              <div className="flex gap-2 text-[9px] font-medium text-neutral-400">
                                <span className="bg-[#7C3AED]/10 text-[#7C3AED] px-1 rounded uppercase">{h.mode}</span>
                                <span>{h.date}</span>
                              </div>
                            </div>
                            <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                          </div>
                        ))}
                      </div>
                    )}
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