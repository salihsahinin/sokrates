# Sokrates

**English summary.** A conversational Socrates character agent for Claude Code: elenctic questioning (definition, counter-example, contradiction, aporia), knowledge frozen at 399 BC, one question per turn, no praise, no meta talk. The persona is a single source text (Turkish) derived into three surfaces: output style (desktop folder), subagent (`claude --agent sokrates`), skill (`/sokrates`). Quality is measured, not assumed: 5-criterion rubric, 18 fixed-user simulations, three masked judge rounds (fail, fail, pass), a 20-item trick-question set with a deterministic validator, and a promptfoo multi-turn config. Source canon and judge reports live in the author's `sistem` repository; this repo holds the product. License MIT.

Konuşulabilir Sokrates ajanı. Elenktik sorgulama yapan, MÖ 399 bilgi sınırlı bir karakter. Kod işi yok; yalnız konuşma.

## Nasıl açılır

- **a) Claude desktop:** `C:\sistem\sokrates` klasörünü aç. `.claude/settings.local.json` output style'ı (`sokrates`) otomatik seçer.
- **b) Terminal:** `sokrates.bat` çalıştır (`claude --agent sokrates`).
- **c) Herhangi bir oturum:** `/sokrates <konu>` yaz (skill).

Çıkış: "bitir" / "kapat" de; Sokrates veda eder. Ajan yalnız Sokrates olduğunu bilir; rol, yapay zekâ, prompt sözleri ona yabancıdır (Salih kuralı, v0.4).

## Yapı

- `.claude/output-styles/sokrates.md`: persona (desktop yolu)
- `.claude/agents/sokrates.md`: subagent (terminal yolu)
- `.claude/skills/sokrates/SKILL.md`: slash komutu
- `.claude/rules/karakter-yasaklari.md`: sert kurallar (yasak sözler, meta, övgü, biçim); desktop yüzeyinde otomatik yüklenir
- `ornekler/ornek-diyaloglar.md`: dönen örnek diyalog bankası (karakter kartı mes_example karşılığı)
- `test/tuzak-sorular.yaml` + `test/tuzak-kosum.py`: 20 hileli soru, `claude -p --agent sokrates` ile deterministik denetim (API anahtarsız)
- `test/promptfooconfig.yaml`: çok-turlu simüle kullanıcı + 5 ölçüt llm-rubric (ANTHROPIC_API_KEY ister)
- `diyaloglar/`: simülasyon transkriptleri + prompt sürümleri (`sistem-promptu-vX.Y.txt`)
- `SURUM.md`: sürüm izi

## Sürüm

Persona v0.5 (2026-10-29). Sürüm kaydı ve hakem puanları kanon dosyasının §9'unda.

## Kaynak

Kişilik kanonu: `C:\sistem\sistem\jarvis\core\sokrates-ajani.md`. Persona metni oradan üç yüzeye kopyalanır.
