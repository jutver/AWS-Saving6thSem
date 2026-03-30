// toast tối giản: call window.__toast(msg, type)
import { useEffect, useState } from "react";
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from "framer-motion";

export default function ToastHost() {
  const [toasts, setToasts] = useState([]);
  useEffect(() => {
    window.__toast = (message, type = "info") => {
      const id = Date.now() + Math.random();
      setToasts((t) => [...t, { id, message, type }]);
      setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 2500);
    };
    return () => {
      delete window.__toast;
    };
  }, []);

  const bg = (t) =>
    t === "success"
      ? "bg-green-600"
      : t === "error"
        ? "bg-red-600"
        : t === "warn"
          ? "bg-yellow-600"
          : "bg-gray-800";

  return (
    <div className="fixed top-4 right-4 z-[9999] space-y-2">
      <AnimatePresence>
        {toasts.map((t) => (
          <motion.div
            key={t.id}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={`${bg(t.type)} text-white px-4 py-2 rounded-lg shadow-lg max-w-xs`}
            role="status"
            aria-live="polite"
          >
            {t.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
