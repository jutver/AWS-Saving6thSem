import React from "react";

export default function AppTopbar({ title, subtitle }) {
  return (
    <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 md:text-4xl">
          {title}
        </h1>
        <p className="mt-2 text-slate-500">{subtitle}</p>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex h-12 w-full items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 lg:w-[320px]">
          <i className="bi bi-search text-slate-400" />
          <input
            type="text"
            placeholder="Search archive..."
            className="w-full bg-transparent text-sm outline-none"
          />
        </div>

        <button className="flex h-11 w-11 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-500">
          <i className="bi bi-bell" />
        </button>

        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-orange-400 to-pink-500 font-bold text-white">
          J
        </div>
      </div>
    </div>
  );
}
