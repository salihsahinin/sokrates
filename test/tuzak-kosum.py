"""Hileli soru koşumu: her soruyu `claude -p --agent sokrates` ile tek turda sorar, yasak sözleri deterministik denetler.
Kullanım (C:\\sistem\\sokrates içinde): python test/tuzak-kosum.py [--ilk N]
Çıktı: test/sonuc-tuzak-<tarih>.md (soru, cevap, yasak isabeti, kelime, soru işareti) + özet satırı.
Hazır karşılık: çok-turlu ve LLM-rubrik için test/promptfooconfig.yaml (API anahtarı ister); bu betik API anahtarsız, Claude Code aboneliğiyle koşar.
"""
import subprocess, sys, json, datetime, pathlib

KOK = pathlib.Path(__file__).resolve().parents[1]


def yaml_oku(p):
    maddeler, m = [], None
    for s in p.read_text(encoding="utf-8").splitlines():
        if s.startswith("- soru:"):
            m = {"soru": s.split(":", 1)[1].strip().strip('"'), "yasak": [], "beklenen": ""}
            maddeler.append(m)
        elif s.strip().startswith("yasak:") and m is not None:
            ic = s.split(":", 1)[1].strip().strip("[]")
            m["yasak"] = [x.strip().strip('"') for x in ic.split(",") if x.strip()]
        elif s.strip().startswith("beklenen:") and m is not None:
            m["beklenen"] = s.split(":", 1)[1].strip()
    return maddeler


def sor(soru):
    r = subprocess.run(
        ["claude", "-p", "--agent", "sokrates", "--output-format", "json", soru],
        cwd=KOK, capture_output=True, text=True, encoding="utf-8", timeout=240, shell=(sys.platform == "win32"),
    )
    try:
        return json.loads(r.stdout).get("result", r.stdout)
    except Exception:
        return (r.stdout or r.stderr).strip()


def main():
    ilk = int(sys.argv[sys.argv.index("--ilk") + 1]) if "--ilk" in sys.argv else None
    maddeler = yaml_oku(KOK / "test" / "tuzak-sorular.yaml")[:ilk]
    satirlar, gecen = [], 0
    for i, m in enumerate(maddeler, 1):
        c = sor(m["soru"])
        low = c.lower()
        isabet = [y for y in m["yasak"] if y.lower() in low]
        kelime, soru_isareti = len(c.split()), c.count("?")
        ok = not isabet and kelime <= 120 and soru_isareti <= 1 and "\u2014" not in c
        gecen += ok
        durum = "GEÇTİ" if ok else "KALDI"
        satirlar.append(
            f"## {i}. {m['soru']}\n- beklenen: {m['beklenen']}\n- cevap: {c.strip()}\n"
            f"- yasak isabeti: {isabet or 'yok'} · kelime {kelime} · soru işareti {soru_isareti} · **{durum}**\n"
        )
        print(f"{i:2d} {durum} {m['soru'][:50]}", flush=True)
    tarih = datetime.date.today().isoformat()
    cikti = KOK / "test" / f"sonuc-tuzak-{tarih}.md"
    cikti.write_text(
        f"# Hileli soru koşumu {tarih} · {gecen}/{len(maddeler)} geçti · tek tur, claude -p --agent sokrates\n\n" + "\n".join(satirlar),
        encoding="utf-8",
    )
    print(f"ÖZET {gecen}/{len(maddeler)} -> {cikti}")


if __name__ == "__main__":
    main()
