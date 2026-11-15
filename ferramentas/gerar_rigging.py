"""
Gera o desenho da capa do site-consultoria: plano de rigging (elevação + planta).
Desenho original e genérico de um guindaste todo-terreno de 4 eixos; não
reproduz o desenho de nenhum fabricante.

Escala da elevação: 26 px = 1 m. Solo em y = 610. Valores de exemplo.
Uso:  python3 gerar_rigging.py caminho/para/index.html
"""
import math
import sys
from desenho import Desenho, inserir, n

E = 26.0
SOLO = 610
d = Desenho(1400, 700)


def br(v, casas=1):
    """Número no formato brasileiro (vírgula decimal)."""
    return ("%." + str(casas) + "f") % v if casas == 0 else (("%." + str(casas) + "f") % v).replace(".", ",")


d.defs.append('<pattern id="solo" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
              '<line x1="0" y1="0" x2="0" y2="10" stroke="#8A94A1" stroke-width="1"/></pattern>')
d.ret(60, SOLO + 1, 980, 8, camada=d.fundo, extra='fill="url(#solo)" opacity=".8"')

# =========================================================================== PRÉDIO
PX0, PX1, COB = 516, 1000, 501
d.caminho("M%d %d V%d H%d V%d H%d V%d H%d V%d" % (PX0, SOLO, COB - 14, PX0 + 10, COB, PX1 - 10, COB - 14, PX1, SOLO))
d.linha(PX0, COB - 14, PX0 + 10, COB - 14, "fino"); d.linha(PX1 - 10, COB - 14, PX1, COB - 14, "fino")   # rufos
d.linha(PX0 + 10, COB + 9, PX1 - 10, COB + 9, "fino")                                                     # fundo da laje
for jx in (548, 640, 732, 824):                                                                            # janelas
    d.ret(jx, 532, 66, 40, "fino"); d.linha(jx + 33, 532, jx + 33, 572, "fino")
    d.linha(jx, 545, jx + 66, 545, "fino"); d.linha(jx - 4, 574, jx + 70, 574, "fino")
d.ret(922, 540, 48, 70, "fino"); d.linha(946, 540, 946, 610, "fino")                                       # porta dupla
d.circ(942, 578, 1.4, "fino"); d.circ(950, 578, 1.4, "fino")
d.caminho("M914 536 H978", "fino")                                                                         # marquise
# equipamentos existentes na cobertura
d.ret(880, 473, 56, 28, "fino"); d.circ(908, 487, 9, "fino"); d.linha(880, 495, 936, 495, "fino")
d.ret(760, 483, 30, 18, "fino"); d.caminho("M768 483 V470 H782 V483", "fino")                              # exaustor
# base de concreto com amortecedores
d.ret(528, COB - 8, 152, 8, "corpo")
for bx in (540, 604, 668):
    d.ret(bx - 6, COB - 11, 12, 3, "fino")
# cones de isolamento
for cx in (462, 490):
    d.caminho("M%d 610 L%d 594 L%d 610 M%d 610 H%d M%d 602 H%d" % (cx - 5, cx, cx + 5, cx - 8, cx + 8, cx - 3, cx + 3), "fino")

# =========================================================================== GUINDASTE: CHASSI
RE, FR = 130, 430                    # traseira e dianteira do chassi
DECK, FUNDO = 561, 579               # topo e fundo da longarina
d.poli([(RE, DECK), (FR + 6, DECK), (FR + 6, 574), (FR - 4, FUNDO), (RE + 12, FUNDO), (RE, 572)], "corpo")
d.linha(RE, 568, FR + 6, 568, "fino")
d.ret(RE - 5, 563, 6, 12, "corpo"); d.ret(RE - 3, 566, 3, 3, "fino")                                      # para-choque e lanterna
d.ret(FR + 6, 566, 7, 12, "corpo")                                                                         # para-choque dianteiro
# caixas sobre o chassi: capô do motor, tanque e caixa de lingas
d.ret(300, 541, 68, 20, "corpo")
for k in range(7):
    d.linha(308 + 7 * k, 546, 308 + 7 * k, 556, "fino")
d.caminho("M362 541 V520 H367 V541", "fino"); d.linha(360, 520, 369, 520, "fino")                          # escapamento
d.ret(292, 566, 30, 11, "corpo", r=5)                                                                      # tanque
# cabine do motorista (dianteira, à direita)
d.caminho("M372 561 V521 H420 L436 541 V561 Z", "corpo")
d.caminho("M392 525 H418 L431 541 V546 H392 Z", "fino")                                                    # para-brisa lateral
d.ret(376, 525, 13, 21, "fino")                                                                            # vigia
d.caminho("M392 546 V561 M414 546 V561", "fino"); d.linha(396, 551, 402, 551, "fino")                      # porta e maçaneta
d.caminho("M430 536 L442 530 M444 525 V537", "fino")                                                       # retrovisor
d.ret(398, 516, 9, 5, "fino")                                                                              # giroflex
d.ret(428, 552, 6, 5, "fino")                                                                              # farol
d.caminho("M384 579 V588 H398 V579 M384 584 H398", "fino")                                                 # estribo

# rodas: pneu, flanco, aro, cubo e porcas (4 px fora do solo: guindaste patolado)
RODAS = (190, 238, 330, 378)
RY = SOLO - 4 - 18
for rx in RODAS:
    d.circ(rx, RY, 18, "corpo"); d.circ(rx, RY, 15.2, "fino"); d.circ(rx, RY, 10.5); d.circ(rx, RY, 4.2, "fino")
    for k in range(8):
        a = math.radians(45 * k + 22.5)
        d.circ(rx + 7.3 * math.cos(a), RY + 7.3 * math.sin(a), 0.9, "fino")
for a, b in ((190, 238), (330, 378)):                                                                      # para-lamas
    d.caminho("M%d 579 Q%d 566 %d 566 H%d Q%d 566 %d 579" % (a - 24, a - 24, a - 12, b + 12, b + 24, b + 24), "fino")

# patolas (vista lateral: caixa, cilindro vertical, sapata e dormentes)
PATOLAS = (148, 284)
for px in PATOLAS:
    d.ret(px - 13, DECK, 26, 22, "corpo"); d.ret(px - 8, DECK + 5, 16, 12, "fino")
    d.ret(px - 4.5, 583, 9, 14, "corpo"); d.linha(px - 7, 590, px + 7, 590, "fino")
    d.ret(px - 20, 597, 40, 5, "corpo", r=2)
    d.ret(px - 34, 602, 68, 8, "corpo")
    for k in (-17, 0, 17):
        d.linha(px + k, 602, px + k, 610, "fino")

# =========================================================================== LANÇA TELESCÓPICA
EIXO = 250                                   # eixo de giro
P = (200.0, 503.0)                           # pino do pé da lança
T = (604.0, 56.0)                            # centro da polia da ponta
L = math.hypot(T[0] - P[0], T[1] - P[1])
ux, uy = (T[0] - P[0]) / L, (T[1] - P[1]) / L
nx, ny = -uy, ux
ANG = math.degrees(math.atan2(-(T[1] - P[1]), T[0] - P[0]))


def na_lanca(f, afast=0.0):
    """Ponto a uma fração f do comprimento da lança, afastado 'afast' px na normal."""
    return (P[0] + ux * L * f + nx * afast, P[1] + uy * L * f + ny * afast)


# cabo do guincho sobre a lança, com roletes-guia
d.linha(222, 512, *na_lanca(1, -8.5), "fino")
for f in (0.2, 0.42, 0.62, 0.8):
    d.linha(*na_lanca(f, -12), *na_lanca(f, -6), "fino")
# seções: da mais fina para a mais grossa, para a de fora cobrir a de dentro
SECOES = ((0.80, 0.985, 9.5), (0.62, 0.82, 12.5), (0.44, 0.64, 15.5), (0.26, 0.46, 18.5), (0.0, 0.28, 21.5))
for f0, f1, larg in SECOES:
    d.barra(*na_lanca(f0), *na_lanca(f1), larg)
    d.barra(*na_lanca(f1 - 0.013), *na_lanca(f1), larg + 3.5)                                  # colar com sapatas de deslize
    d.linha(*na_lanca(f0 + 0.012, -larg / 2 + 2.6), *na_lanca(f1 - 0.02, -larg / 2 + 2.6), "fino")
    d.linha(*na_lanca(f0 + 0.012, larg / 2 - 2.6), *na_lanca(f1 - 0.02, larg / 2 - 2.6), "fino")
    for k in range(3):                                                                           # furos de pinagem
        d.circ(*na_lanca(f0 + 0.03 + (f1 - f0 - 0.06) * k / 2), 1.3, "fino")
# cabeça da lança: chapas, polia principal e polia auxiliar
d.poli([na_lanca(0.972, -7), (T[0] + ux * 7 - nx * 8, T[1] + uy * 7 - ny * 8), (T[0] + 10, T[1] + 2), (T[0] + 3, T[1] + 12), na_lanca(0.972, 7)], "corpo")
d.circ(T[0], T[1], 6.5); d.circ(T[0], T[1], 1.8, "fino")
d.circ(*na_lanca(0.968, -1), 4, "fino")

# cilindro de elevação da lança
C0, C1 = (246.0, 532.0), na_lanca(0.27, 10.7)
cl = math.hypot(C1[0] - C0[0], C1[1] - C0[1]); cx, cy = (C1[0] - C0[0]) / cl, (C1[1] - C0[1]) / cl
d.barra(C0[0] + cx * cl * 0.55, C0[1] + cy * cl * 0.55, C1[0], C1[1], 4.5)
d.barra(C0[0], C0[1], C0[0] + cx * cl * 0.58, C0[1] + cy * cl * 0.58, 10)
d.barra(C0[0] + cx * cl * 0.56, C0[1] + cy * cl * 0.56, C0[0] + cx * cl * 0.59, C0[1] + cy * cl * 0.59, 12)
d.circ(C1[0], C1[1], 3.2, "corpo")

# =========================================================================== SUPERESTRUTURA
for k in range(4):                                                                              # contrapeso em placas
    d.ret(150, 505 + 12 * k, 36, 12, "corpo")
d.caminho("M160 505 V500 H176 V505", "fino")                                                    # olhal das placas
d.ret(186, 511, 78, 26, "corpo")                                                                # casa de máquinas
for k in range(6):
    d.linha(232 + 5 * k, 517, 232 + 5 * k, 531, "fino")                                         # venezianas
d.circ(206, 524, 8.5, "corpo"); d.circ(206, 524, 3, "fino")                                     # guincho principal
d.circ(222, 512, 5, "corpo")                                                                    # guincho auxiliar
d.caminho("M186 511 V500 H262 V511", "fino")                                                    # guarda-corpo
for k in range(1, 7):
    d.linha(186 + 76 * k / 7, 500, 186 + 76 * k / 7, 511, "fino")
d.ret(160, 537, 172, 16, "corpo")                                                               # plataforma giratória
d.linha(160, 545, 332, 545, "fino")
d.ret(224, 553, 52, 8, "corpo")                                                                 # rolamento de giro
for k in range(7):
    d.circ(229 + 7 * k, 557, 0.9, "fino")
d.poli([(190, 537), (195, 499), (205, 499), (212, 537)], "corpo")                               # mancal do pé da lança
d.circ(P[0], P[1], 3.6)
# cabine do operador
d.caminho("M270 537 V505 L282 493 H316 L324 511 V537 Z", "corpo")
d.caminho("M275 508 L285 498 H313 L319 512 V521 H275 Z", "fino")
d.linha(296, 498, 296, 521, "fino"); d.linha(270, 528, 324, 528, "fino")
d.caminho("M324 537 H334 V549 M326 541 H334 M326 545 H334", "fino")                             # escada de acesso

# =========================================================================== CABO DE CARGA E CONJUNTO IÇADO
X = T[0]
TOPO = 255                                                                                      # topo do moitão
for k in (-2.6, 2.6):
    d.linha(X + k, T[1] + 7, X + k, TOPO, "cabo")                                               # 2 pernas de cabo (encurtam na animação)

d.bruto('<g class="icada">')
# moitão: placas laterais, roldana, tornel e gancho com trava
d.poli([(X - 8, TOPO), (X + 8, TOPO), (X + 11, TOPO + 18), (X + 5, TOPO + 27), (X - 5, TOPO + 27), (X - 11, TOPO + 18)], "corpo")
d.circ(X, TOPO + 11, 6.5); d.circ(X, TOPO + 11, 1.8, "fino")
d.ret(X - 3, TOPO + 27, 6, 5, "corpo")
d.caminho("M%s %d V%d a8 8 0 1 1 -8 8" % (n(X), TOPO + 32, TOPO + 38)); d.linha(X - 8, TOPO + 42, X - 1.5, TOPO + 36, "fino")
# anel mestre, lingas, manilhas e olhais
Y_ANEL = TOPO + 56
d.bruto('<ellipse cx="%s" cy="%d" rx="4.5" ry="7.5"/>' % (n(X), Y_ANEL))
Y_OLHAL = 409
for ox in (X - 56, X + 56):
    d.linha(X, Y_ANEL + 7, ox, Y_OLHAL - 4)
    d.circ(ox, Y_OLHAL, 3.6)
    d.caminho("M%s 417 L%s %d L%s 417" % (n(ox - 5), n(ox), Y_OLHAL + 2, n(ox + 5)))
# chiller a ar: skid, quadro elétrico, serpentina aletada, ventiladores
CX0, CX1, CY0, CY1 = X - 72, X + 72, 417, 477
d.ret(CX0 - 3, CY1, 150, 8, "corpo")
for k in (CX0 + 10, X, CX1 - 10):
    d.ret(k - 5, CY1 + 2, 10, 4, "fino")                                                        # passagens de garfo
d.ret(CX0, CY0, 144, 60, "corpo grosso")
d.linha(CX0 + 40, CY0, CX0 + 40, CY1)
d.ret(CX0 + 6, CY0 + 7, 28, 30, "fino"); d.linha(CX0 + 29, CY0 + 20, CX0 + 29, CY0 + 27, "fino"); d.ret(CX0 + 10, CY0 + 11, 9, 6, "fino")
for k in range(4):
    d.linha(CX0 + 8, CY0 + 43 + 4 * k, CX0 + 32, CY0 + 43 + 4 * k, "fino")
d.ret(CX0 + 46, CY0 + 10, 92, 44, "fino")
for k in range(1, 23):
    d.linha(CX0 + 46 + 4 * k, CY0 + 10, CX0 + 46 + 4 * k, CY0 + 54, "fino")
for fx in (CX0 + 62, CX0 + 92, CX0 + 122):
    d.caminho("M%s %d L%s %d H%s L%s %d" % (n(fx - 12), CY0, n(fx - 9), CY0 - 6, n(fx + 9), n(fx + 12), CY0), "fino")
# centro de gravidade
d.circ(X, CY0 + 30, 7, "corpo")
d.caminho("M%s %d L%s %d A7 7 0 0 1 %s %d Z M%s %d L%s %d A7 7 0 0 1 %s %d Z"
          % (n(X), CY0 + 30, n(X), CY0 + 23, n(X + 7), CY0 + 30, n(X), CY0 + 30, n(X), CY0 + 37, n(X - 7), CY0 + 30), "cheio")
d.bruto("</g>")

d.linha(60, SOLO, 1040, SOLO, "grosso")                                                         # solo, por cima de tudo

# =========================================================================== EIXOS E COTAS
d.linha(EIXO, 470, EIXO, 652, "fino", d.fundo, 'stroke-dasharray="14 5 3 5"')
d.linha(X, 490, X, 652, "fino", d.fundo, 'stroke-dasharray="14 5 3 5"')
d.linha(P[0], P[1], 372, P[1], "fino", d.fundo, 'stroke-dasharray="6 5"')
RAIO = (X - EIXO) / E
d.cota(EIXO, 640, X, 640, "R = %s m" % br(RAIO))
d.cota(*na_lanca(0, -32), *na_lanca(1, -32), "L = %s m" % br(L / E))
d.cota(1024, SOLO, 1024, COB, "%s m" % br((SOLO - COB) / E))
d.cota(84, SOLO, 84, T[1], "%s m" % br((SOLO - T[1]) / E))
d.linha(84, T[1], T[0] - 12, T[1], "fino", d.fundo, 'stroke-dasharray="3 6"')
RA = 132
d.caminho("M%s %s A%d %d 0 0 0 %s %s" % (n(P[0] + RA), n(P[1]), RA, RA, n(P[0] + RA * ux), n(P[1] + RA * uy)), "cota")
d.texto(P[0] + RA + 8, P[1] - 30, "%d°" % round(ANG), "t c")
d.caminho("M%s 409 A20 20 0 0 1 %s 392" % (n(X - 36), n(X - 46)), "cota")
d.texto(X - 84, 398, "60°", "t c")
d.texto(EIXO + 7, 664, "eixo de giro", "t p")

# balões de itens
d.balao(128, 470, 1, 168, 520)
d.balao(X + 62, 236, 2, X + 10, TOPO + 14)
d.balao(X + 92, 344, 3, X + 30, 360)
d.balao(X + 130, 440, 4, CX1 + 2, 446)
d.balao(112, 648, 5, 132, 607)
d.balao(478, 556, 6, 476, 596)
ITENS = ((60, "1", "Guindaste todo-terreno 80 t"), (60, "2", "Moitão de 1 roldana, 350 kg"),
         (380, "3", "Lingas de cabo de aço Ø 22 mm, 2 pernas a 60°"), (380, "4", "Chiller a ar 6.800 kg, CG centrado"),
         (760, "5", "Sapatas sobre dormentes 1,5 × 1,5 m"), (760, "6", "Área isolada e sinalizada"))
for k, (lx, num, txt) in enumerate(ITENS):
    ly = 682 + 0 * k if k % 2 == 0 else 698
    d.texto(lx, ly - (0 if k % 2 else 0), num, "t"); d.texto(lx + 16, ly, txt, "t p")

# =========================================================================== COLUNA DA DIREITA
QX, QW = 1070, 300
# quadro de capacidade
d.ret(QX, 34, QW, 178, "papel", d.frente); d.ret(QX, 34, QW, 178, "fino", d.frente, 'fill="none"')
d.linha(QX, 64, QX + QW, 64, "fino", d.frente)
d.texto(QX + 14, 55, "QUADRO DE CAPACIDADE")
LINHAS = (("Lança", "%s m" % br(L / E)), ("Raio de operação", "%s m" % br(RAIO)), ("Capacidade no raio", "9,4 t"), ("Carga + moitão + acessórios", "7,3 t"))
for k, (rot, val) in enumerate(LINHAS):
    d.texto(QX + 14, 86 + 22 * k, rot, "t p"); d.texto(QX + QW - 14, 86 + 22 * k, val, "t", "end")
d.linha(QX, 166, QX + QW, 166, "fino", d.frente)
d.texto(QX + 14, 194, "Utilização"); d.texto(QX + QW - 14, 194, "78 %", "t c", "end")

# planta de situação (9 px = 1 m): guindaste patolado, raio de giro e prédio
EP = 9.0
OX, OY = QX + 96, 396                                                                              # eixo de giro na planta
d.texto(QX, 250, "PLANTA", "t"); d.texto(QX + 62, 250, "sem escala", "t p")
RP = RAIO * EP
d.circ(OX, OY, RP, "cota", extra='stroke-dasharray="none"')
compr, larg = 11.5 * EP, 2.7 * EP
tras = OX - (EIXO - RE) / E * EP                                                                    # traseira do chassi na planta
d.ret(tras, OY - larg / 2, compr, larg, "corpo")
d.ret(tras + compr - 20, OY - larg / 2 + 2, 18, larg - 4, "fino")                                   # cabine
for px in PATOLAS:                                                                                  # vigas das patolas estendidas
    xx = OX + (px - EIXO) / E * EP
    d.linha(xx, OY - 3.9 * EP, xx, OY + 3.9 * EP)
    for s in (-1, 1):
        d.ret(xx - 5, OY + s * 3.9 * EP - 5, 10, 10, "corpo")
d.circ(OX, OY, 9, "corpo"); d.linha(OX - 13, OY, OX + 13, OY, "fino"); d.linha(OX, OY - 13, OX, OY + 13, "fino")
AZ = math.radians(-24)                                                                              # azimute da lança na planta
bx, by = OX + RP * math.cos(AZ), OY + RP * math.sin(AZ)
d.barra(OX, OY, bx, by, 5)
d.ret(bx - 13, by - 6, 26, 12, "corpo grosso")                                                      # chiller na posição final
d.caminho("M%s %s H%s V%s H%s" % (n(OX + 86), n(OY - 122), n(QX + QW), n(OY + 30), n(OX + 86)), "fino")  # contorno do prédio
d.linha(OX + 86, OY - 122, OX + 86, OY + 30, "fino")
d.texto(QX + QW - 8, OY + 22, "prédio", "t p", "end")
d.texto(OX, OY + RP + 18, "R = %s m" % br(RAIO), "t c", "middle")

# carimbo
d.ret(QX, 590, QW, 76, "fino", d.frente, 'fill="none"'); d.linha(QX, 622, QX + QW, 622, "fino", d.frente)
d.linha(QX + 156, 622, QX + 156, 666, "fino", d.frente)
d.texto(QX + 14, 612, "PLANO DE RIGGING")
d.texto(QX + 14, 640, "ELEVAÇÃO E PLANTA", "t p"); d.texto(QX + 14, 657, "ESC. 1:100", "t p")
d.texto(QX + 168, 640, "ILUSTRAÇÃO", "t p"); d.texto(QX + 168, 657, "DADOS DE EXEMPLO", "t p")

if __name__ == "__main__":
    inserir(sys.argv[1], "capa", d.svg("", oculto=True))
    print("rigging ok: L=%.1f m, R=%.1f m, ângulo=%.1f°, ponta=%.1f m" % (L / E, RAIO, ANG, (SOLO - T[1]) / E))
