import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import os

import sys
sys.path.append("C:/Users/Ritik Koshta/Desktop/QLearning")


# OBSTICALS = [...]  # your full OBSTICALS list here
from QuardupleAgent.Assays.Mega_glu import OBSTICALS , Start_1, Start_2, Start_3, Start_4, GRID_DIM_C, GRID_DIM_R, Name, FOOTPRINT_1, FOOTPRINT_2, FOOTPRINT_3, FOOTPRINT_4

# 4 start positions
STARTS = [Start_1, Start_2, Start_3, Start_4]

# 4 action strings
ACTIONS = [
    "00023300000333333120333331111133220242022244121032030010000000432222003030000433200403022130000114211304134240320000033332241211434114343311111332442222214120000203000000402222224214433141111303332332331333431111433111132113220313333333331111132120120333411210113044322404100034122022242111112333332300300303333111113300220000004002222000000022113340404201343313300000223143104022221202431102030000033332243222222222222222224000200023022300002222233334301312232403110000000222223333333224332104224424222301111211140324333420133330200330043433333333333343111113324122034342222223334443341321020222322101144411122333203333143000320024331402223422233243222114113124221022242000320042322324430311111101013102004000231104114001002223",  # Agent 1
    "03002200000234222221203120422221111130313303004011104000400000333333312220022200000020002031302000004311114132102222221111101211111111131111111222222000002222122033321322000400022222221303333311133411442432111132243311220041112301002210440224211040302330230003342000022333313403433014343022241200000002342000033221302413033433110000040202333333333433333333330201220022010000200030221343024422314300133433311110044322332222323203434200322112332303411131010133022411004020404222222221220241130100332321114231111112114222222224221130211100024131112231423043333103311141234400321402011403032010102340110103420212242244210424222111110300333004300404440104022423334111320042131212124241211112222220000022221202321300000033332222222222",  # Agent 2
    "41113333333111111304221311131100000033433111113222242022111300002000222211111223343303423310334202111241111133111411213031241112113300200003343331414111422223211002004020400414232220040300433333333334021000000323333300000333331103032200000222223141111333331304333114111332222140102211111132324224232222242322121111211322111140221221002301323340210313300000030402001000004401334100043334333330431433334333333340000033324212111222122221211111223221141111202433312420311112130300003333411111320020220223022223222111112333331140003240200430031422244442121144112223222012224202222220201411233043404131341013311411121111002300222313431011112133043322321220423422221111122433333310010331110133403300000021023314110002324223224011224311",  # Agent 3 (dummy)
    "13112222222111112130312111311200332024002303310333111321133022222222000022221111142422222001132000004222221203320000033333333333333324222220124222222122022242222333333134033333303313333322022120313334333411114113102143112111121141222222222222222311114001411130104221310302000100000100200000030300241402312232332413203431201202222141100333330010010404004233324224012222423333321434431110112012304422300143434134212104111413224021434342131321411301041111111131422310403333311111302222222114133040002000222221101111223324333331230243333033313334334303200040343334311040401222133031141121243123420331300123113132312141222222222330333331141111233212022333110330222222211411011333304301341141122001400222242222220000022222213000000222",  # Agent 4 (dummy)
]

# 4 footprints (list of edge tuples)
FOOTPRINTS = [
    FOOTPRINT_1,  # Replace with FOOTPRINT_1
    FOOTPRINT_2,  # Replace with FOOTPRINT_2
    FOOTPRINT_3,  # Optional: define for Agent 3
    FOOTPRINT_4   # Optional: define for Agent 4
]

# Colors for each agent
AGENT_COLORS = ['red', 'purple', 'orange', 'deepskyblue']
FOOTPRINT_COLORS = ['lightskyblue', 'plum', 'lightcoral', 'lightgreen']
START_COLORS = ['royalblue', 'darkviolet', 'saddlebrown', 'navy']


class RenderMultiAgent:
    def __init__(self, grid_size, starts, footprints, obstacles):
        self.grid_size = grid_size
        self.starts = starts
        self.footprints = footprints
        self.obstacles = obstacles
        self.frames = []
        self.paths = [[] for _ in starts]
        self.output_dir = f"{Name}/output_frames"
        os.makedirs(self.output_dir, exist_ok=True)

    def add_frame(self, positions, t):
        for i, pos in enumerate(positions):
            self.paths[i].append(pos)

        fig, ax = plt.subplots()
        ax.set_xlim(0, self.grid_size[1])
        ax.set_ylim(0, self.grid_size[0])
        ax.set_aspect('equal')

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if (i in [0, self.grid_size[0] - 1] or j in [0, self.grid_size[1] - 1]) and (i, j) not in self.starts:
                    color = 'gray'
                else:
                    color = 'white'
                ax.add_patch(patches.Rectangle((j, i), 1, 1, edgecolor='black', facecolor=color))

        # Footprints
        for idx, fp_list in enumerate(self.footprints):
            for (p1, p2) in fp_list:
                for p in [p1, p2]:
                    ax.add_patch(patches.Rectangle((p[1], p[0]), 1, 1, edgecolor='black', facecolor=FOOTPRINT_COLORS[idx]))

        # Obstacles
        if t < len(self.obstacles):
            for ob in self.obstacles[t]:
                ax.add_patch(patches.Rectangle((ob[1], ob[0]), 1, 1, edgecolor='black', facecolor='green'))
                plt.text(ob[1]+0.5, ob[0]+0.5, str(t), fontsize=6, ha='center', va='center', color='white')

        # Paths
        for idx, path in enumerate(self.paths):
            if len(path) > 1:
                px = [p[1] + 0.5 for p in path]
                py = [p[0] + 0.5 for p in path]
                ax.plot(px, py, color=AGENT_COLORS[idx], linewidth=2, marker='o')

        # Start cells
        for idx, s in enumerate(self.starts):
            ax.add_patch(patches.Rectangle((s[1], s[0]), 1, 1, edgecolor='black', facecolor=START_COLORS[idx]))

        # Current agent positions
        for idx, p in enumerate(positions):
            if p != self.starts[idx]:
                ax.add_patch(patches.Rectangle((p[1], p[0]), 1, 1, edgecolor='black', facecolor=AGENT_COLORS[idx]))
                plt.text(p[1] + 0.5, p[0] + 0.95, str(t), fontsize=6, ha='center', va='top', color='white')

        plt.text(self.grid_size[1]/2, self.grid_size[0]+0.5, f"Frame {len(self.frames)+1}", ha='center')
        plt.axis('off')

        path = os.path.join(self.output_dir, f"frame_{len(self.frames)+1}.png")
        plt.savefig(path, bbox_inches='tight')
        plt.close()

        img = imageio.imread(path)
        self.frames.append(img)
        print(f"Frame {len(self.frames)} saved")

    def save_gif(self, filename="agents.gif"):
        path = os.path.join(self.output_dir, filename)
        imageio.mimsave(path, self.frames, duration=1000.0)
        print(f"GIF saved to {path}")


def simulate_multi_agents(actions, starts, footprints, obstacles, grid_size):
    direction_map = {
        '0': (1, 0), '1': (-1, 0), '2': (0, -1), '3': (0, 1), '4': (0, 0)
    }

    min_r, max_r = 1, grid_size[0] - 2
    min_c, max_c = 1, grid_size[1] - 2
    pos = list(starts)

    r = RenderMultiAgent(grid_size, starts, footprints, obstacles)
    r.add_frame(pos, t=0)

    max_len = max(len(a) for a in actions)

    for t in range(1, max_len + 1):
        for idx in range(len(actions)):
            if t - 1 < len(actions[idx]):
                move = direction_map.get(actions[idx][t - 1], (0, 0))
                cand = (pos[idx][0] + move[0], pos[idx][1] + move[1])

                if not (min_r <= pos[idx][0] <= max_r and min_c <= pos[idx][1] <= max_c):
                    if min_r <= cand[0] <= max_r and min_c <= cand[1] <= max_c:
                        pos[idx] = cand
                elif min_r <= cand[0] <= max_r and min_c <= cand[1] <= max_c:
                    pos[idx] = cand

        r.add_frame(pos, t)

    r.save_gif()


# ------------------- MAIN ------------------- #

if __name__ == "__main__":
    simulate_multi_agents(ACTIONS, STARTS, FOOTPRINTS, OBSTICALS, (GRID_DIM_R, GRID_DIM_C))
