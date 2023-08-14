from hackingPackage.overlay import FullScreenOverlay, Draw
from hackingPackage.csgoInterface import LocalPlayer, get_players, world_to_screen
from hackingPackage.io import is_pressed


def wall_hack(should_run):
    with FullScreenOverlay() as overlay:
        while should_run.is_set():
            me = LocalPlayer()
            my_team = me.get_team()
            my_health = me.get_health()
            my_view_matrix = me.get_view_matrix()

            for player in get_players():
                if me.base == player.base:
                    continue
                if my_team == player.get_team():
                    continue
                health = player.get_health()
                if my_health < 1 or health < 1:
                    continue

                xy_head = world_to_screen(player.get_head_pos(), my_view_matrix)
                xy_base = world_to_screen(player.get_pos(), my_view_matrix)
                if not xy_head or not xy_base:
                    continue

                height = abs(xy_head[1] - xy_base[1])

                if xy_base[0] < xy_head[0]:
                    x_min = xy_base[0] - 0.25 * height
                    x_max = xy_head[0] + 0.25 * height
                    y_min = xy_base[1] - 0.15 * height
                    y_max = xy_head[1] + 0.15 * height

                else:
                    x_min = xy_head[0] - 0.25 * height
                    x_max = xy_base[0] + 0.25 * height
                    y_min = xy_base[1] - 0.15 * height
                    y_max = xy_head[1] + 0.15 * height

                # draw box and line to player
                Draw.outline(x_min, y_min, x_max - x_min, y_max - y_min, 0.1, Draw.red)
                Draw.line((x_max + x_min) / 2, y_min, 960, 0, 0.1, Draw.white)

                # draw head
                if is_pressed(0x6):
                    Draw.circle(xy_head[0], xy_head[1], height * 0.02, Draw.red)

                # draw health
                health_x = x_max + height * 0.1
                health_y = y_min + height * 1.3 * health * 0.01
                Draw.line(health_x, y_min, health_x, health_y, height * 0.01, Draw.green)
                Draw.line(health_x, health_y, health_x, y_max, height * 0.01, Draw.red)

            overlay.update()


if __name__ == '__main__':
    import threading
    run_flag = threading.Event()
    run_flag.set()
    wall_hack(run_flag)
