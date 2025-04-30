import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import os

# ------------------- SETUP ------------------- #

Name = "assayPCR8x15"
GRID_DIM_R = 10
GRID_DIM_C = 17

Start_1 = (9, 1)
Start_2 = (9, 15)

Action_1 = "11333333411222222113133031120303300302202142220111102141431142"
Action_2 = "11204221111111220040032031343300130322222111413222113333330000"


OBSTICALS = [
    [], 
    [(3, 1), (1, 2), (1, 5), (1, 11), (1, 14), (3, 15)],
    [(4, 1), (1, 2), (2, 5), (2, 11), (1, 14), (4, 15)],
    [(5, 1), (2, 2), (3, 5), (3, 11), (2, 14), (5, 15)],
    [(5, 2), (2, 2), (3, 6), (3, 10), (2, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (4, 2), (3, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 2), (2, 2), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (5, 14)],
    [(6, 2), (2, 3), (3, 7), (3, 8), (3, 9), (3, 10), (2, 14), (6, 14)],
    [(7, 2), (2, 4), (4, 7), (4, 10), (2, 14), (7, 14)],
    [(7, 1), (3, 4), (5, 7), (5, 10), (2, 14), (7, 15)],
    [(3, 5), (6, 7), (5, 11), (2, 14)],
    [(1, 8), (3, 6), (7, 7), (5, 12), (2, 14)],
    [(1, 9), (3, 7), (7, 6), (5, 13), (2, 14)],
    [(1, 10), (3, 7), (7, 5), (5, 14), (2, 14)],
    [(2, 10), (3, 7), (7, 4), (5, 14), (4, 14), (3, 14), (2, 14)],
    [(3, 10), (3, 7), (7, 3), (5, 14), (4, 14), (3, 14), (2, 14)],
    [(3, 10), (3, 9), (3, 8), (3, 7), (7, 2), (5, 14), (4, 14), (3, 14), (2, 14)],
    [(3, 10), (3, 9), (3, 8), (3, 7), (7, 1), (5, 14), (4, 14), (3, 14), (2, 14)],
    [(3, 10), (3, 9), (3, 8), (3, 7), (5, 14), (4, 14), (3, 14), (2, 14)],
    [(3, 10), (3, 9), (3, 8), (3, 7), (5, 14), (4, 14), (3, 14), (2, 14)],
    [(3, 10), (3, 9), (3, 8), (3, 7), (5, 14), (2, 14)],
    [(3, 10), (3, 9), (3, 8), (3, 7), (5, 14), (2, 14)],
    [(3, 10), (3, 7), (6, 14), (2, 14)],
    [(3, 10), (3, 7), (7, 14), (2, 14)],
    [(4, 10), (4, 7), (7, 15), (2, 14)],
    [(5, 10), (5, 7), (2, 14)],
    [(5, 11), (6, 7), (2, 14)],
    [(5, 12), (7, 7), (2, 14)],
    [(5, 13), (7, 6), (2, 14)],
    [(5, 14), (7, 5), (2, 14)],
    [(7, 4), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(1, 11), (7, 3), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(1, 12), (7, 2), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(2, 12), (7, 1), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(3, 12), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(4, 12), (2, 14), (3, 14), (4, 14), (5, 14)],
    [(5, 12), (2, 14), (5, 14)],
    [(5, 12), (2, 14), (5, 14)],
    [(5, 12), (2, 14), (6, 14)],
    [(5, 12), (2, 14), (7, 14)],
    [(5, 13), (2, 14), (7, 15)],
    [(5, 14), (2, 14)],
    [(5, 14), (4, 14), (3, 14), (2, 14)],
    [(5, 14), (4, 14), (3, 14), (2, 14)],
    [(5, 14), (4, 14), (3, 14), (2, 14)],
    [(5, 14), (4, 14), (3, 14), (2, 14)],
    [(5, 14), (4, 14), (3, 14), (2, 14)],
    [(5, 14), (4, 14), (3, 14), (2, 14)],
    [(5, 14), (2, 14)],
    [(5, 14), (2, 14)],
    [(6, 14), (3, 14)],
    [(7, 14), (4, 14)],
    [(8, 14), (5, 14)],
    [(8, 13), (6, 14)],
    [(6, 15)],
    [(7, 15)],
    []
]


FOOTPRINT_1 = [
        ((2,2),(2,3)),
        ((2,3),(2,4)),
        ((2,4),(2,5)),
        ((3,1),(3,2)),
        ((3,4),(3,5)),
        ((3,5),(3,6)),
        ((3,6),(3,7)),
        ((4,1),(4,2)),
        ((5,1),(5,2)),
        ((7,1),(7,2)),
        ((7,2),(7,3)),
        ((7,3),(7,4)),
        ((7,4),(7,5)),
        ((7,5),(7,6)),
        ((7,6),(7,7)),
        ((3,1),(4,1)),
        ((4,1),(5,1)),
        ((1,2),(2,2)),
        ((2,2),(3,2)),
        ((3,2),(4,2)),
        ((4,2),(5,2)),
        ((5,2),(6,2)),
        ((6,2),(7,2)),
        ((2,4),(3,4)),
        ((1,5),(2,5)),
        ((2,5),(3,5)),
        ((3,7),(4,7)),
        ((4,7),(5,7)),
        ((5,7),(6,7)),
        ((6,7),(7,7))
    ]
FOOTPRINT_2 = [
            ((1,8),(1,9)),
        ((1,9),(1,10)),
        ((1,10),(1,11)),
        ((1,11),(1,12)),
        ((3,7),(3,8)), 
        ((3,8),(3,9)),
        ((3,9),(3,10)),
        ((3,10),(3,11)),
        ((3,11),(3,12)),
        ((3,14),(3,15)),
        ((5,10),(5,11)),
        ((5,11),(5,12)),
        ((5,12),(5,13)),
        ((5,13),(5,14)),
        ((6,14),(6,15)),
        ((7,14),(7,15)),
        ((8,13),(8,14)),
        ((1,10),(2,10)),
        ((2,10),(3,10)),
        ((3,10),(4,10)),
        ((4,10),(5,10)),
        ((1,12),(2,12)),
        ((2,12),(3,12)),
        ((3,12),(4,12)),
        ((4,12),(5,12)),
        ((1,14),(2,14)),
        ((2,14),(3,14)),
        ((3,14),(4,14)),
        ((4,14),(5,14)),
        ((5,14),(6,14)),
        ((6,14),(7,14)),
        ((7,14),(8,14)),
        ((6,15),(7,15))
    ]


# FOOTPRINT_1 and FOOTPRINT_2 from your message
# OBSTICALS from your message
# (Omitted here for brevity – include them at the top of the file)

# ------------------- RENDER CLASS ------------------- #

class Render:
    def __init__(self, grid_size, footprints_1, footprints_2, obstacles):
        self.grid_size = grid_size
        self.footprints_1 = footprints_1
        self.footprints_2 = footprints_2
        self.obstacles = obstacles
        self.frames = []
        self.path_1 = []
        self.path_2 = []
        self.output_dir = f"{Name}/output_frames"
        os.makedirs(self.output_dir, exist_ok=True)
        self.start_1 = None
        self.start_2 = None

    def add_frame(self, pos1, pos2, t):
        if len(self.path_1) == 0:
            self.start_1 = pos1
            self.start_2 = pos2

        self.path_1.append(pos1)
        self.path_2.append(pos2)

        fig, ax = plt.subplots()
        ax.set_xlim(0, self.grid_size[1])
        ax.set_ylim(0, self.grid_size[0])
        ax.set_aspect('equal')

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if (i in [0, self.grid_size[0] - 1] or j in [0, self.grid_size[1] - 1]) and (i, j) not in [self.start_1, self.start_2]:
                    color = 'gray'
                else:
                    color = 'white'
                ax.add_patch(patches.Rectangle((j, i), 1, 1, edgecolor='black', facecolor=color))

        for fp in self.footprints_1:
            for p in fp:
                ax.add_patch(patches.Rectangle((p[1], p[0]), 1, 1, edgecolor='black', facecolor='lightskyblue'))

        for fp in self.footprints_2:
            for p in fp:
                ax.add_patch(patches.Rectangle((p[1], p[0]), 1, 1, edgecolor='black', facecolor='plum'))

        if t < len(self.obstacles):
            for ob in self.obstacles[t]:
                ax.add_patch(patches.Rectangle((ob[1], ob[0]), 1, 1, edgecolor='black', facecolor='green'))
                plt.text(ob[1] + 0.5, ob[0] + 0.5, str(t), fontsize=7, ha='center', va='center', color='white')

        def draw_path(path, color):
            if len(path) > 1:
                px = [p[1] + 0.5 for p in path]
                py = [p[0] + 0.5 for p in path]
                ax.plot(px, py, color=color, linestyle='-', linewidth=2, marker='o')

        draw_path(self.path_1, 'red')
        draw_path(self.path_2, 'blue')

        ax.add_patch(patches.Rectangle((self.start_1[1], self.start_1[0]), 1, 1, edgecolor='black', facecolor='royalblue'))
        ax.add_patch(patches.Rectangle((self.start_2[1], self.start_2[0]), 1, 1, edgecolor='black', facecolor='darkviolet'))

        if pos1 != self.start_1:
            ax.add_patch(patches.Rectangle((pos1[1], pos1[0]), 1, 1, edgecolor='black', facecolor='red'))
            plt.text(pos1[1] + 0.5, pos1[0] + 0.95, str(t), fontsize=7, ha='center', va='top', color='white')

        if pos2 != self.start_2:
            ax.add_patch(patches.Rectangle((pos2[1], pos2[0]), 1, 1, edgecolor='black', facecolor='purple'))
            plt.text(pos2[1] + 0.5, pos2[0] + 0.95, str(t), fontsize=7, ha='center', va='top', color='white')

        plt.text(self.grid_size[1]/2, self.grid_size[0]+0.5, f'Frame: {len(self.frames)+1}', ha='center')
        plt.axis('off')

        path = os.path.join(self.output_dir, f'frame_{len(self.frames)+1}.png')
        plt.savefig(path, bbox_inches='tight')
        plt.close()

        img = imageio.imread(path)
        self.frames.append(img)
        print(f"Frame {len(self.frames)} saved")

    def save_gif(self, name='agents.gif'):
        out = os.path.join(self.output_dir, name)
        imageio.mimsave(out, self.frames, duration=1000.0)
        print(f"Saved final GIF: {out}")

# ------------------- SIMULATION ------------------- #

def simulate_dual_agents(action1, action2, start1, start2, footprints1, footprints2, obstacles, grid_size):
    direction_map = {
        '0': (1, 0),  '1': (-1, 0), '2': (0, -1), '3': (0, 1), '4': (0, 0)
    }

    min_r, max_r = 1, grid_size[0] - 2
    min_c, max_c = 1, grid_size[1] - 2

    r = Render(grid_size, footprints1, footprints2, obstacles)
    pos1, pos2 = start1, start2

    r.add_frame(pos1, pos2, t=0)

    for t in range(1, max(len(action1), len(action2)) + 1):
        # Agent 1
        if t - 1 < len(action1):
            move = direction_map.get(action1[t - 1], (0, 0))
            cand = (pos1[0] + move[0], pos1[1] + move[1])
            if not (min_r <= pos1[0] <= max_r and min_c <= pos1[1] <= max_c):
                if min_r <= cand[0] <= max_r and min_c <= cand[1] <= max_c:
                    pos1 = cand
            elif min_r <= cand[0] <= max_r and min_c <= cand[1] <= max_c:
                pos1 = cand

        # Agent 2
        if t - 1 < len(action2):
            move = direction_map.get(action2[t - 1], (0, 0))
            cand = (pos2[0] + move[0], pos2[1] + move[1])
            if not (min_r <= pos2[0] <= max_r and min_c <= pos2[1] <= max_c):
                if min_r <= cand[0] <= max_r and min_c <= cand[1] <= max_c:
                    pos2 = cand
            elif min_r <= cand[0] <= max_r and min_c <= cand[1] <= max_c:
                pos2 = cand

        r.add_frame(pos1, pos2, t)

    r.save_gif()

# ------------------- MAIN ------------------- #

if __name__ == "__main__":
    simulate_dual_agents(Action_1, Action_2, Start_1, Start_2, FOOTPRINT_1, FOOTPRINT_2, OBSTICALS, (GRID_DIM_R, GRID_DIM_C))
