import { useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type TabType = "general" | "account" | "personalisation" | "billing" | "notification" | "api";

type NotificationCategory = "communication" | "reminder" | "announcement";
type NotificationChannel = "email" | "desktop" | "push";

interface NotificationSettings {
  email: boolean;
  desktop: boolean;
  push: boolean;
}

// ─── Primitives ───────────────────────────────────────────────────────────────

const Toggle = ({ checked, onChange }: { checked: boolean; onChange: (v: boolean) => void }) => (
  <button
    role="switch"
    aria-checked={checked}
    onClick={() => onChange(!checked)}
    className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
      checked ? "bg-sky-400" : "bg-gray-200"
    }`}
  >
    <span
      className={`inline-block h-3.5 w-3.5 rounded-full bg-white shadow transition-transform ${
        checked ? "translate-x-4" : "translate-x-1"
      }`}
    />
  </button>
);

const CheckBox = ({ checked, onChange }: { checked: boolean; onChange: (v: boolean) => void }) => (
  <button
    role="checkbox"
    aria-checked={checked}
    onClick={() => onChange(!checked)}
    className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${
      checked ? "bg-sky-400 border-sky-400" : "bg-white border-gray-300"
    }`}
  >
    {checked && (
      <svg className="w-2.5 h-2.5 text-white" viewBox="0 0 10 8" fill="none">
        <path d="M1 4l3 3 5-6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    )}
  </button>
);

const PasswordInput = ({ value }: { value: string }) => {
  const [visible, setVisible] = useState(false);
  return (
    <div className="relative">
      <input
        type={visible ? "text" : "password"}
        defaultValue={value}
        className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg pr-10 focus:outline-none focus:ring-1 focus:ring-sky-300"
      />
      <button
        onClick={() => setVisible(!visible)}
        className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
      >
        {visible ? (
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" />
            <line x1="1" y1="1" x2="23" y2="23" />
          </svg>
        ) : (
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
        )}
      </button>
    </div>
  );
};

const TextInput = ({ value }: { value: string }) => (
  <input
    defaultValue={value}
    className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-sky-300"
  />
);

const FieldRow = ({ label, children }: { label: string; children: React.ReactNode }) => (
  <div className="flex flex-col gap-1.5">
    <label className="text-sm text-gray-500 capitalize">{label}</label>
    {children}
  </div>
);

// ─── Tab Panels ───────────────────────────────────────────────────────────────

const GeneralTab = () => {
  const [loginEnabled, setLoginEnabled] = useState(true);
  const [language, setLanguage] = useState("default");
  const [media, setMedia] = useState({ photo: true, audio: true, video: true, document: false });

  return (
    <div className="space-y-1 divide-y divide-gray-100">
      <Row label="Login">
        <div className="flex items-center gap-2">
          <Toggle checked={loginEnabled} onChange={setLoginEnabled} />
          <span className="text-sm text-gray-500">{loginEnabled ? "On" : "Off"}</span>
        </div>
      </Row>

      <Row label="Language">
        <div className="relative">
          <svg className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" />
            <path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" />
          </svg>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="pl-8 pr-3 py-1.5 text-sm bg-slate-50 border border-slate-200 rounded-lg appearance-none focus:outline-none focus:ring-1 focus:ring-sky-300"
          >
            <option value="default">Default</option>
            <option value="en">English</option>
            <option value="uk">Ukrainian</option>
            <option value="es">Spanish</option>
          </select>
        </div>
      </Row>

      <Row label="Media permissions">
        <div className="flex flex-col gap-1.5">
          {(Object.keys(media) as Array<keyof typeof media>).map((key) => (
            <label key={key} className="flex items-center gap-2 cursor-pointer">
              <CheckBox checked={media[key]} onChange={(v) => setMedia((p) => ({ ...p, [key]: v }))} />
              <span className="text-sm text-gray-600 capitalize">{key}</span>
            </label>
          ))}
        </div>
      </Row>

      <Row label="Messages">
        <button className="px-3 py-1.5 text-sm text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
          Archive all
        </button>
      </Row>
    </div>
  );
};

const Row = ({ label, children }: { label: string; children: React.ReactNode }) => (
  <div className="flex items-center justify-between py-3">
    <span className="text-sm text-gray-500">{label}</span>
    {children}
  </div>
);

const AccountTab = () => (
  <div className="space-y-4">
    <FieldRow label="Username"><TextInput value="Sylvia Reyes" /></FieldRow>
    <FieldRow label="Birthday"><TextInput value="19/10/1994" /></FieldRow>
    <FieldRow label="Email"><TextInput value="sylvia@mercure.studio" /></FieldRow>
    <FieldRow label="Password"><PasswordInput value="password123456" /></FieldRow>
  </div>
);

const NotificationRow = ({
  title,
  description,
  settings,
  onChange,
}: {
  title: string;
  description: string;
  settings: NotificationSettings;
  onChange: (key: NotificationChannel, value: boolean) => void;
}) => (
  <div className="flex items-start justify-between py-4 border-t border-gray-100">
    <div className="max-w-xs">
      <p className="text-sm font-medium text-gray-800">{title}</p>
      <p className="text-xs text-gray-400 mt-0.5">{description}</p>
    </div>
    <div className="flex flex-col gap-1.5">
      {(["email", "desktop", "push"] as NotificationChannel[]).map((key) => (
        <label key={key} className="flex items-center gap-2 cursor-pointer">
          <Toggle checked={settings[key]} onChange={(v) => onChange(key, v)} />
          <span className="text-xs text-gray-500 capitalize">{key}</span>
        </label>
      ))}
    </div>
  </div>
);

const NotificationTab = () => {
  const [notifications, setNotifications] = useState<Record<NotificationCategory, NotificationSettings>>({
    communication: { email: true, desktop: true, push: true },
    reminder: { email: false, desktop: true, push: true },
    announcement: { email: false, desktop: false, push: false },
  });

  const update = (cat: NotificationCategory, key: NotificationChannel, value: boolean) =>
    setNotifications((p) => ({ ...p, [cat]: { ...p[cat], [key]: value } }));

  return (
    <div className="space-y-4">
      <div className="bg-sky-50 border border-sky-100 rounded-lg p-4 flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-gray-800">Important notifications</p>
          <p className="text-xs text-gray-500 mt-0.5">We may still send you important notifications about your account.</p>
          <div className="flex gap-4 mt-2">
            <button className="text-xs text-sky-500 hover:underline">Dismiss</button>
            <button className="text-xs text-sky-500 hover:underline">Learn more</button>
          </div>
        </div>
        <svg className="w-5 h-5 text-sky-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
      </div>

      <NotificationRow
        title="Communication"
        description="Receive notifications for comments, tags, change requests and new activity."
        settings={notifications.communication}
        onChange={(k, v) => update("communication", k, v)}
      />
      <NotificationRow
        title="Reminder"
        description="Reminders for updates you might have missed."
        settings={notifications.reminder}
        onChange={(k, v) => update("reminder", k, v)}
      />
      <NotificationRow
        title="Announcement and update"
        description="Product updates, newest features, improvements and bug fixes."
        settings={notifications.announcement}
        onChange={(k, v) => update("announcement", k, v)}
      />
    </div>
  );
};

const PlaceholderTab = ({ title }: { title: string }) => (
  <p className="text-sm text-gray-400">{title} — coming soon.</p>
);

// ─── Tabs config ──────────────────────────────────────────────────────────────

const TABS: { id: TabType; label: string; badge?: number }[] = [
  { id: "general", label: "General" },
  { id: "account", label: "Account" },
  { id: "personalisation", label: "Personalisation" },
  { id: "billing", label: "Billing" },
  { id: "notification", label: "Notification", badge: 2 },
  { id: "api", label: "API" },
];

// ─── Root ─────────────────────────────────────────────────────────────────────

const ProfileForm = () => {
  const [activeTab, setActiveTab] = useState<TabType>("general");

  const renderContent = () => {
    switch (activeTab) {
      case "general": return <GeneralTab />;
      case "account": return <AccountTab />;
      case "notification": return <NotificationTab />;
      case "personalisation": return <PlaceholderTab title="Personalisation" />;
      case "billing": return <PlaceholderTab title="Billing" />;
      case "api": return <PlaceholderTab title="API" />;
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-xl overflow-hidden">
      {/* Banner */}
      <div className="relative h-32 bg-gradient-to-br from-sky-100 via-sky-50 to-teal-50 overflow-hidden">
        <svg className="absolute inset-0 w-full h-full" viewBox="0 0 400 120" preserveAspectRatio="xMidYMid slice">
          <polygon points="200,0 400,60 400,120 200,60" fill="rgba(14,165,233,0.08)" />
          <polygon points="250,0 400,40 400,80 250,40" fill="rgba(14,165,233,0.06)" />
          <polygon points="150,20 300,80 300,120 150,60" fill="rgba(20,184,166,0.05)" />
        </svg>
      </div>

      {/* Profile header */}
      <div className="px-6 -mt-12 relative z-10">
        <div className="flex items-end gap-4">
          <div className="relative">
            <div className="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center text-3xl font-medium text-gray-500 border-4 border-white shadow-sm">
              S
            </div>
            <span className="absolute -bottom-1 -right-1 w-6 h-6 bg-sky-400 rounded-full border-2 border-white flex items-center justify-center">
              <svg className="w-3 h-3 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </span>
          </div>

          <div className="flex-1 flex items-center justify-between pb-2">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">Sylvia Reyes</h1>
              <p className="text-sm text-gray-400">+44 656 548 060</p>
            </div>
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
                Log out
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
                </svg>
              </button>
              <button className="p-1.5 text-gray-400 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="5" cy="12" r="1.5" /><circle cx="12" cy="12" r="1.5" /><circle cx="19" cy="12" r="1.5" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mt-6 border-b border-gray-100">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-2 text-sm font-medium rounded-t-lg transition-colors flex items-center gap-1.5 ${
                activeTab === tab.id
                  ? "bg-sky-50 text-sky-600 border border-sky-200 border-b-0"
                  : "text-gray-500 hover:text-gray-800 hover:bg-gray-50"
              }`}
            >
              {tab.label}
              {tab.badge && (
                <span className="px-1.5 py-0.5 text-xs bg-sky-100 text-sky-600 rounded">
                  {tab.badge}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <h2 className="text-base font-semibold text-gray-800 mb-5">
          {TABS.find((t) => t.id === activeTab)?.label}
        </h2>
        {renderContent()}
      </div>
    </div>
  );
};

export default ProfileForm;
