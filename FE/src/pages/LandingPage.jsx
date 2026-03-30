import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const fadeUp = {
  hidden: { opacity: 0, y: 28 },
  show: (delay = 0) => ({
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.7,
      delay,
      ease: [0.22, 1, 0.36, 1],
    },
  }),
};

const fadeIn = {
  hidden: { opacity: 0 },
  show: (delay = 0) => ({
    opacity: 1,
    transition: {
      duration: 0.8,
      delay,
      ease: "easeOut",
    },
  }),
};

const floating = {
  animate: {
    y: [0, -10, 0],
    transition: {
      duration: 4.5,
      repeat: Infinity,
      ease: "easeInOut",
    },
  },
};

const floatingSlow = {
  animate: {
    y: [0, 12, 0],
    x: [0, 8, 0],
    transition: {
      duration: 8,
      repeat: Infinity,
      ease: "easeInOut",
    },
  },
};

export default function LandingPage() {
  return (
    <div className="relative overflow-hidden bg-[#f6f7fb] pb-10 pt-6">
      <motion.div
        variants={floatingSlow}
        animate="animate"
        className="pointer-events-none absolute -left-16 top-16 h-72 w-72 rounded-full bg-indigo-200/40 blur-3xl"
      />
      <motion.div
        variants={floating}
        animate="animate"
        className="pointer-events-none absolute right-[-40px] top-[220px] h-80 w-80 rounded-full bg-sky-200/30 blur-3xl"
      />
      <motion.div
        variants={floatingSlow}
        animate="animate"
        className="pointer-events-none absolute bottom-10 left-1/3 h-56 w-56 rounded-full bg-violet-200/30 blur-3xl"
      />

      <div className="mx-auto w-[95%] max-w-7xl">
        <motion.header
          initial="hidden"
          animate="show"
          custom={0}
          variants={fadeUp}
          className="sticky top-4 z-20 flex items-center justify-between rounded-2xl border border-slate-200/80 bg-white/80 px-6 py-4 backdrop-blur-xl"
        >
          <div className="text-sm font-bold text-indigo-600 md:text-base">
            Sound Capture
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="text-sm font-semibold text-slate-700 transition hover:text-indigo-600"
            >
              Login
            </Link>
            <Link
              to="/dashboard"
              className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow transition duration-300 hover:-translate-y-0.5 hover:bg-indigo-700 hover:shadow-lg"
            >
              Get Started
            </Link>
          </div>
        </motion.header>

        <section className="mt-7 grid gap-8 rounded-3xl border border-slate-200 bg-white/85 p-6 backdrop-blur-sm md:p-10 lg:grid-cols-2">
          <motion.div
            initial="hidden"
            animate="show"
            variants={fadeIn}
            custom={0.1}
            className="flex flex-col justify-center"
          >
            <motion.h1
              variants={fadeUp}
              initial="hidden"
              animate="show"
              custom={0.1}
              className="text-4xl font-black leading-tight text-slate-900 md:text-6xl"
            >
              Transcribe,
              <br />
              Analyze, & Master
              <br />
              Your
              <br />
              <span className="text-indigo-600">Conversations</span>
            </motion.h1>

            <motion.p
              variants={fadeUp}
              initial="hidden"
              animate="show"
              custom={0.22}
              className="mt-6 max-w-xl text-base leading-7 text-slate-500"
            >
              Experience the ethereal power of AI that does not just listen, but
              understands. Turn every meeting, interview, and voice note into a
              searchable, actionable database of intelligence.
            </motion.p>

            <motion.div
              variants={fadeUp}
              initial="hidden"
              animate="show"
              custom={0.34}
              className="mt-8 flex flex-wrap gap-4"
            >
              <Link
                to="/dashboard"
                className="rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white shadow transition duration-300 hover:-translate-y-0.5 hover:bg-indigo-700 hover:shadow-lg"
              >
                Get Started Free
              </Link>

              <button
                onClick={() => {
                  const el = document.getElementById("features");
                  if (el) {
                    el.scrollIntoView({ behavior: "smooth" });
                  }
                }}
                className="rounded-xl bg-slate-100 px-5 py-3 font-semibold text-slate-700 transition duration-300 hover:-translate-y-0.5 hover:bg-slate-200 hover:shadow-md"
              >
                Learn More
              </button>
            </motion.div>

            <motion.div
              variants={fadeUp}
              initial="hidden"
              animate="show"
              custom={0.46}
              className="mt-8 flex flex-wrap gap-3"
            >
              <div className="rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700">
                AI Summary
              </div>
              <div className="rounded-full border border-sky-100 bg-sky-50 px-4 py-2 text-sm font-medium text-sky-700">
                Speaker Detection
              </div>
              <div className="rounded-full border border-violet-100 bg-violet-50 px-4 py-2 text-sm font-medium text-violet-700">
                Action Items
              </div>
            </motion.div>
          </motion.div>

          <motion.div
            initial="hidden"
            animate="show"
            variants={fadeUp}
            custom={0.28}
            className="flex items-center justify-center"
          >
            <div className="relative flex w-full max-w-[520px] gap-4">
              <motion.div
                animate={{
                  y: [0, -8, 0],
                }}
                transition={{
                  duration: 5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="flex-1 rounded-2xl bg-white p-4 shadow-xl ring-1 ring-slate-100"
              >
                <div className="mb-4 space-y-2">
                  <div className="h-1.5 w-20 rounded-full bg-indigo-200" />
                  <div className="h-1.5 w-28 rounded-full bg-slate-200" />
                </div>

                <div className="relative h-52 overflow-hidden rounded-xl bg-[radial-gradient(circle_at_center,_rgba(255,210,120,0.8),_rgba(80,70,220,0.35)_45%,_#111827_80%)]">
                  <motion.div
                    animate={{
                      opacity: [0.35, 0.7, 0.35],
                      scale: [1, 1.08, 1],
                    }}
                    transition={{
                      duration: 4,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                    className="absolute left-1/2 top-1/2 h-28 w-28 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/30"
                  />
                  <motion.div
                    animate={{
                      opacity: [0.2, 0.5, 0.2],
                      scale: [1, 1.18, 1],
                    }}
                    transition={{
                      duration: 4,
                      delay: 0.6,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                    className="absolute left-1/2 top-1/2 h-40 w-40 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/20"
                  />
                  <motion.div
                    animate={{
                      opacity: [0.12, 0.35, 0.12],
                      scale: [1, 1.28, 1],
                    }}
                    transition={{
                      duration: 4,
                      delay: 1.1,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                    className="absolute left-1/2 top-1/2 h-52 w-52 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10"
                  />
                </div>
              </motion.div>

              <motion.div
                animate={{
                  y: [0, 10, 0],
                }}
                transition={{
                  duration: 5.8,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="flex w-[110px] flex-col gap-4"
              >
                <motion.div
                  whileHover={{ y: -4, scale: 1.02 }}
                  className="flex h-40 flex-col items-center justify-center rounded-2xl bg-indigo-100 text-center text-slate-500 shadow"
                >
                  <i className="bi bi-stars text-xl text-indigo-500" />
                  <span className="mt-2 text-sm font-medium">AI Insights</span>
                </motion.div>

                <motion.div
                  whileHover={{ y: -4, scale: 1.02 }}
                  className="flex h-28 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow"
                >
                  <i className="bi bi-mic-fill text-xl" />
                </motion.div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.8, duration: 0.6 }}
                className="absolute -bottom-6 left-10 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-lg"
              >
                <div className="text-xs font-bold tracking-[0.18em] text-slate-400">
                  LIVE SUMMARY
                </div>
                <div className="mt-1 text-sm font-semibold text-slate-800">
                  3 action items detected
                </div>
              </motion.div>
            </div>
          </motion.div>
        </section>
        <section
          id="features"
          className="mt-8 rounded-3xl bg-[#f9fafe] px-4 py-14 md:px-8"
        >
          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            variants={fadeUp}
            custom={0}
            className="text-center text-[11px] font-extrabold tracking-[0.25em] text-indigo-500"
          >
            MAIN FEATURES
          </motion.div>

          <motion.h2
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            variants={fadeUp}
            custom={0.1}
            className="mt-3 text-center text-3xl font-black text-slate-900 md:text-4xl"
          >
            Perfect for Business
          </motion.h2>

          <div className="mt-10 grid gap-5 md:grid-cols-3">
            {[
              {
                icon: "bi-file-earmark-text",
                title: "Crystal Clear Transcription",
                text: "Capture every nuance with high accuracy. Handle complex accents, industry jargon, and multi-speaker environments with ease.",
                iconClass: "bg-indigo-100 text-indigo-600",
              },
              {
                icon: "bi-stars",
                title: "Deep Analysis & Summarization",
                text: "Get automated summaries, sentiment analysis, and key takeaway extraction in seconds.",
                iconClass: "bg-sky-100 text-sky-600",
              },
              {
                icon: "bi-magic",
                title: "AI Editing Assistant",
                text: "Transform spoken content into polished text. Clean filler words, improve clarity, and produce structured outputs.",
                iconClass: "bg-slate-100 text-slate-600",
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true, amount: 0.2 }}
                variants={fadeUp}
                custom={index * 0.12}
                whileHover={{ y: -6 }}
                className="rounded-2xl border border-slate-200 bg-white p-6 transition-shadow duration-300 hover:shadow-xl"
              >
                <div
                  className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${feature.iconClass}`}
                >
                  <i className={`bi ${feature.icon}`} />
                </div>
                <h3 className="text-lg font-bold">{feature.title}</h3>
                <p className="mt-3 text-sm leading-6 text-slate-500">
                  {feature.text}
                </p>
              </motion.div>
            ))}
          </div>
        </section>

        <motion.section
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.25 }}
          variants={fadeUp}
          custom={0}
          className="mt-8"
        >
          <div className="relative overflow-hidden rounded-[28px] bg-indigo-600 px-6 py-14 text-center text-white shadow-xl">
            <motion.div
              animate={{
                x: [0, 20, 0],
                y: [0, -10, 0],
              }}
              transition={{
                duration: 8,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="absolute -left-10 top-0 h-40 w-40 rounded-full bg-white/10 blur-2xl"
            />

            <motion.div
              animate={{
                x: [0, -18, 0],
                y: [0, 14, 0],
              }}
              transition={{
                duration: 9,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="absolute bottom-0 right-0 h-44 w-44 rounded-full bg-white/10 blur-2xl"
            />

            <h2 className="relative text-3xl font-black leading-tight md:text-5xl">
              Ready to turn your audio into
              <br />
              your most valuable asset?
            </h2>

            <Link
              to="/login"
              className="relative mt-8 inline-block rounded-xl bg-white px-6 py-3 font-semibold text-indigo-600 transition duration-300 hover:-translate-y-0.5 hover:shadow-lg"
            >
              Create Your Free Account
            </Link>
          </div>
        </motion.section>
      </div>
    </div>
  );
}
