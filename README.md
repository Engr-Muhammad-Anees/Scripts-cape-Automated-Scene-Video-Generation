#  Automated AI Video Generation Pipeline

An end-to-end **script-to-video automation pipeline** that transforms a written script into a fully synchronized, subtitle-embedded video using **LLMs, diffusion-based image models, TTS, alignment logic, and FFmpeg**.

This project is designed to be **modular, scalable, and mostly free-tier friendly**, making it ideal for experimentation, research, and automation-focused content generation.

---

##  Project Overview

This pipeline automates the entire video creation workflow:

1. Script → Scenes (LLM)
2. Scenes → Image Prompts (Python logic)
3. Prompts → Images (Hugging Face Diffusion – Free Tier)
4. Scenes → Audio Style Metadata
5. Scene-wise Audio Generation (`.wav`)
6. Subtitle Generation with Phrase-by-Phrase Alignment (`.srt`)
7. Scene + Audio Video Assembly
8. Subtitle Overlay + Visual Effects (FFmpeg)
9. Final Video Output 

---

##  High-Level Architecture

```text
Script
  ↓
Scene Generation (OpenRouter LLM)
  ↓
Image Prompt Builder (Python)
  ↓
Image Generation (HF Diffusion API)
  ↓
Audio Style Extraction
  ↓
Audio Generation (Scene-wise WAV and using ELEVENLAB API)
  ↓
Subtitle Generation (Forced Alignment)
  ↓
Scene Video Creation
  ↓
FFmpeg Effects + Subtitle Burn-in
  ↓
Final Video
