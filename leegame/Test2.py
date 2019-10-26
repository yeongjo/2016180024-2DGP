import pico2d as tt

tt.open_canvas()
print(tt.get_canvas_height())
tt.canvas_height = 10
print(tt.get_canvas_height())