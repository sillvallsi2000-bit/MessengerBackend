import { useState } from "react";
import LeftPanelForm from "../../components/Chat/LeftPanelForm";
import CallsList, { Call } from "../../components/Calls/CallsLisForm";
import LogoIcon from "../../assets/leftside/Logo.svg";

const mockCalls: Call[] = [
  { id: "1",  name: "Francis",  dateTime: "Yesterday, 15:03",   type: "outgoing" },
  { id: "2",  name: "Leila",    avatar: "https://i.pravatar.cc/150?img=5",  dateTime: "Yesterday, 15:22",   type: "incoming" },
  { id: "3",  name: "Sam",      avatar: "https://i.pravatar.cc/150?img=12", dateTime: "Yesterday, 17:46",   type: "missed",   missedCount: 2 },
  { id: "4",  name: "Isabella", avatar: "https://i.pravatar.cc/150?img=9",  dateTime: "05/02/24, 09:21",    type: "outgoing" },
  { id: "5",  name: "Susan",    dateTime: "04/02/24, 20:55",   type: "incoming" },
  { id: "6",  name: "Lana",     avatar: "https://i.pravatar.cc/150?img=20", dateTime: "04/02/24, 22:43",    type: "incoming" },
  { id: "7",  name: "Paul",     dateTime: "06/02/24, 15:03",   type: "missed" },
  { id: "8",  name: "Bastien",  avatar: "https://i.pravatar.cc/150?img=33", dateTime: "06/02/24, 15:22",    type: "missed" },
  { id: "9",  name: "Oumy",     avatar: "https://i.pravatar.cc/150?img=25", dateTime: "06/02/24, 17:46",    type: "incoming" },
  { id: "10", name: "Sarah",    avatar: "https://i.pravatar.cc/150?img=32", dateTime: "06/02/24, 09:21",    type: "incoming" },
  { id: "11", name: "Daniel",   dateTime: "06/02/24, 20:55",   type: "outgoing" },
  { id: "12", name: "Alice",    avatar: "https://i.pravatar.cc/150?img=44", dateTime: "06/02/24, 22:43",    type: "incoming" },
];

// ─── Layout (відповідає ContactsLayout) ───────────────────────────────────────

type CallsLayoutProps = {
  children: React.ReactNode;
  leftPanel: React.ReactNode;
  detailPanel?: React.ReactNode;
};

export const CallsLayout = ({ children, leftPanel, detailPanel }: CallsLayoutProps) => {
  return (
    <div className="flex h-screen w-full">
      {/* Ліва вузька панель (іконки навігації) */}
      <div className="flex-[0.5] bg-gray-100">
        {leftPanel}
      </div>

      {/* Основний контент */}
      <div className="flex-[9.5] bg-gray-50 flex gap-4 p-4">
        {/* Список дзвінків */}
        <div className="flex-[2.5] bg-white rounded-xl overflow-hidden">
          {children}
        </div>

        {/* Деталі / порожній стан */}
        <div className="flex-[7.5] bg-white rounded-xl overflow-hidden">
          {detailPanel}
        </div>
      </div>
    </div>
  );
};

// ─── Порожній стан для правої панелі ──────────────────────────────────────────

const CallsEmptyDetail = () => (
  <div className="flex flex-col items-center justify-center h-full gap-4">
    <img src={LogoIcon} alt="Messenger" className="w-32 h-32 opacity-20" />
    <h2 className="text-xl font-medium text-gray-400">Messenger</h2>
    <p className="text-sm text-gray-400">
      Your personal calls are end-to-end encrypted
    </p>
  </div>
);

// ─── Сторінка (використовує CallsLayout так само як ContactsLayout) ────────────

const CallsPage = () => {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <CallsLayout
      leftPanel={<LeftPanelForm />}
      detailPanel={<CallsEmptyDetail />}
    >
      <CallsList
        calls={mockCalls}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />
    </CallsLayout>
  );
};

export default CallsPage;
