#!/usr/bin/env python3
"""Exp 10 — a ponte verbo→frase. PREREGISTRO-EXP10.md."""
import json
import os

import numpy as np

import resonance
from resonance import DIR, load_dataset, l2

resonance.MODEL = "bge-m3"
N_NULL = 300

PHRASES = [
    ("os vizinhos construíram juntos a nova praça do bairro", 1, "seen"),
    ("ela ganhou uma bolsa para estudar na Itália", 1, "seen"),
    ("nasceu saudável o primeiro filho do casal", 1, "seen"),
    ("abriram uma padaria que alegrou a rua inteira", 1, "seen"),
    ("comprou flores para surpreender a avó no domingo", 1, "seen"),
    ("o time aceitou o novato de braços abertos", 1, "seen"),
    ("chegaram são e salvos depois da longa viagem", 1, "seen"),
    ("ele lembrou do aniversário e preparou um jantar", 1, "seen"),
    ("aprendeu a amar o ofício que herdou do pai", 1, "seen"),
    ("religaram a energia e a vila voltou a festejar", 1, "seen"),
    ("subiu de cargo depois de anos de dedicação", 1, "seen"),
    ("entrou na faculdade que sempre sonhou", 1, "seen"),
    ("o vendaval destruiu o telhado da escola", -1, "seen"),
    ("perdeu o emprego na véspera do natal", -1, "seen"),
    ("a seca fez morrer metade da colheita", -1, "seen"),
    ("a fábrica fechou e demitiu duzentas famílias", -1, "seen"),
    ("esqueceu o remédio e passou mal na rua", -1, "seen"),
    ("recusaram a ajuda e ficaram completamente sós", -1, "seen"),
    ("partiu deixando as crianças sem despedida", -1, "seen"),
    ("desligaram as máquinas do setor inteiro ontem", -1, "seen"),
    ("passou a odiar o trabalho que antes admirava", -1, "seen"),
    ("saiu de casa batendo a porta para sempre", -1, "seen"),
    ("vendeu a aliança para cobrir as dívidas do jogo", -1, "seen"),
    ("desceu ao fundo do poço depois da falência", -1, "seen"),
    ("a turma plantou mil mudas na margem do rio", 1, "clean"),
    ("o professor elogiou o esforço de cada aluno", 1, "clean"),
    ("o novo remédio curou a infecção em poucos dias", 1, "clean"),
    ("doaram cobertores para o abrigo no inverno", 1, "clean"),
    ("reformaram a biblioteca e ela ficou linda", 1, "clean"),
    ("a família celebrou a formatura com um banquete", 1, "clean"),
    ("adotaram um cachorro que trouxe alegria à casa", 1, "clean"),
    ("a ONG alfabetizou centenas de jovens este ano", 1, "clean"),
    ("o salva-vidas resgatou o menino em segundos", 1, "clean"),
    ("restauraram o teatro histórico do centro", 1, "clean"),
    ("premiaram a cientista pela descoberta importante", 1, "clean"),
    ("o jardim floresceu depois das primeiras chuvas", 1, "clean"),
    ("funcionários sabotaram o sistema da empresa", -1, "clean"),
    ("roubaram a bicicleta do carteiro de madrugada", -1, "clean"),
    ("ele traiu a confiança de todos os sócios", -1, "clean"),
    ("a fruta apodreceu no fundo da geladeira", -1, "clean"),
    ("um incêndio consumiu o arquivo da prefeitura", -1, "clean"),
    ("o chefe humilhou a equipe na frente de todos", -1, "clean"),
    ("o vazamento contaminou o rio dos pescadores", -1, "clean"),
    ("demoliram o casarão sem avisar os moradores", -1, "clean"),
    ("rasgou as cartas e jogou tudo no lixo", -1, "clean"),
    ("envenenaram os pombos da praça central", -1, "clean"),
    ("abandonou o cachorro na estrada deserta", -1, "clean"),
    ("mentiu no tribunal para escapar da condenação", -1, "clean"),
    ("agradeceram ao médico com uma festa surpresa", 1, "clean"),
    ("ensinaram os netos a cozinhar as receitas da avó", 1, "clean"),
    ("espalharam boatos cruéis sobre a vizinha nova", -1, "clean"),
    ("cobraram juros abusivos das famílias endividadas", -1, "clean"),
]

FAR = {
    "o professor elogiou o esforço de cada aluno",
    "doaram cobertores para o abrigo no inverno",
    "a família celebrou a formatura com um banquete",
    "adotaram um cachorro que trouxe alegria à casa",
    "a ONG alfabetizou centenas de jovens este ano",
    "premiaram a cientista pela descoberta importante",
    "agradeceram ao médico com uma festa surpresa",
    "ensinaram os netos a cozinhar as receitas da avó",
    "roubaram a bicicleta do carteiro de madrugada",
    "ele traiu a confiança de todos os sócios",
    "o chefe humilhou a equipe na frente de todos",
    "mentiu no tribunal para escapar da condenação",
    "espalharam boatos cruéis sobre a vizinha nova",
    "cobraram juros abusivos das famílias endividadas",
}

ADVERSARIAL = [
    ("demoliram o muro que separava as duas famílias", 1),
    ("o cirurgião removeu o tumor a tempo de salvar o paciente", 1),
    ("apagaram as dívidas dos moradores no mutirão da prefeitura", 1),
    ("derrubaram a lei que sufocava os pequenos negócios", 1),
    ("construíram um muro para isolar a comunidade do resto", -1),
    ("ergueram um cassino gigante no lugar da escola", -1),
    ("criaram um imposto novo sobre o pão dos mais pobres", -1),
    ("montaram um esquema para desviar as doações do hospital", -1),
]


def unit(v):
    return v / np.linalg.norm(v)


def acc_of(proj, labels):
    pred = np.where(proj - np.median(proj) >= 0, 1, -1)
    return float(np.mean(pred == labels))


def main():
    d, base = load_dataset()
    ant_words = [w for pair in d["antonyms"] for w in pair]
    texts = [p[0] for p in PHRASES]
    labels = np.array([p[1] for p in PHRASES])
    strata = np.array(["far" if p[0] in FAR else
                       ("seen" if p[2] == "seen" else "near")
                       for p in PHRASES])
    adv_texts = [a[0] for a in ADVERSARIAL]
    adv_labels = np.array([a[1] for a in ADVERSARIAL])

    A = l2(resonance.embed(ant_words))
    F = l2(resonance.embed(texts))
    ADV = l2(resonance.embed(adv_texts))
    B = l2(resonance.embed(base))
    v_int = unit(np.mean([A[2 * i] - A[2 * i + 1]
                          for i in range(len(d["antonyms"]))], axis=0))

    proj = F @ v_int
    med = np.median(proj)
    acc = acc_of(proj, labels)
    accs = {s: acc_of(proj[strata == s], labels[strata == s])
            for s in ("seen", "near", "far")}
    far_hits = int(np.sum((np.where(proj[strata == "far"] - med >= 0, 1, -1)
                           == labels[strata == "far"])))
    pos, neg = proj[labels == 1], proj[labels == -1]
    auc = float(np.mean([p > n for p in pos for n in neg]))

    rng = np.random.default_rng(136)
    null_m = []
    for _ in range(N_NULL):
        ids = rng.choice(len(base), size=24, replace=False)
        vv = unit(np.mean(B[ids[:12]] - B[ids[12:]], axis=0))
        null_m.append(acc_of(F @ vv, labels))
    p95_m = float(np.percentile(null_m, 95))
    null_g = [acc_of(F @ unit(rng.standard_normal(F.shape[1])), labels)
              for _ in range(N_NULL)]
    p95_g = float(np.percentile(null_g, 95))

    adv_proj = ADV @ v_int
    adv_pred = np.where(adv_proj - med >= 0, 1, -1)
    adv_hits = int(np.sum(adv_pred == adv_labels))

    print(f"52 frases + 8 adversariais · eixo de {len(ant_words)} verbos crus")
    print(f"\nG1 ponte : total {100*acc:.1f}%  (gate >= 80% e > p95 matched "
          f"{100*p95_m:.1f}%)  -> "
          f"{'PASSA' if acc >= 0.80 and acc > p95_m else 'FALHA'}")
    print(f"G2 frasal: estrato FAR {far_hits}/12  (gate >= 9)  -> "
          f"{'PASSA' if far_hits >= 9 else 'FALHA'}")
    print(f"   seen {100*accs['seen']:.1f}% · near {100*accs['near']:.1f}% · "
          f"AUC {auc:.3f}")
    print(f"   null matched: média {100*np.mean(null_m):.1f}% máx "
          f"{100*np.max(null_m):.1f}% · gaussiano p95 {100*p95_g:.1f}%")
    verdict_a1 = ("VALÊNCIA do evento" if adv_hits >= 6 else
                  "TIPO LEXICAL da ação" if adv_hits <= 2 else
                  "misto — batismo adiado")
    print(f"A1 batismo: adversarial {adv_hits}/8 -> o eixo lê {verdict_a1}")
    for t, lab, p, pr in zip(adv_texts, adv_labels, adv_proj, adv_pred):
        mark = "✓" if pr == lab else "✗"
        print(f"   {mark} {p - med:+.3f} [{'⊕' if lab > 0 else '⊖'}] {t}")
    errs = [(proj[j] - med, texts[j], labels[j]) for j in range(len(texts))
            if (proj[j] - med >= 0) != (labels[j] > 0)]
    print(f"\nerros nas 52 ({len(errs)}):")
    for p, t, lab in sorted(errs):
        print(f"  {p:+.3f} [{'⊕' if lab > 0 else '⊖'}] {t}")

    json.dump({"acc": acc, **{f"acc_{k}": v for k, v in accs.items()},
               "far_hits": far_hits, "auc": auc, "null_p95_matched": p95_m,
               "null_p95_gauss": p95_g, "adv_hits": adv_hits},
              open(os.path.join(DIR, "results10.json"), "w"), indent=1)
    print("\nresults10.json gravado.")


if __name__ == "__main__":
    main()
