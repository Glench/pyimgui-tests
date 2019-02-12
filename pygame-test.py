from __future__ import absolute_import

import sys

import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui


def main():
    pygame.init()

    size = 800, 600

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)

    renderer = PygameRenderer()

    io = imgui.get_io()
    io.fonts.add_font_default()
    alt_font = io.fonts.add_font_from_file_ttf("Arial.ttf", 16, io.fonts.get_glyph_ranges_latin())
    renderer.refresh_font_texture()
    io.display_size = size





    def load_image(image_name='test.png'):
        image = pygame.image.load(image_name)
        textureSurface = pygame.transform.flip(image, False, True)

        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)

        width = textureSurface.get_width()
        height = textureSurface.get_height()

        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                     gl.GL_UNSIGNED_BYTE, textureData)

        return texture, width, height

    image_texture, image_width, image_height = load_image('replit.png')


    # state

    text_val = 'test input box here'
    toggle_test_window = False


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            renderer.process_event(event)

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        # imgui.begin("Custom window", True)
        # imgui.text("Bar")
        # imgui.text_colored("Eggs", r=0.2, g=1., b=0.)
        # imgui.end()

        imgui.begin("Glen's notes", True)
        imgui.text("Feb 15, 2019")

        imgui.bullet_text("demo window is good for seeing all functionality:")
        imgui.same_line()
        if imgui.button("show demo window" if not toggle_test_window else "hide demo window"):
            toggle_test_window = not toggle_test_window
        if toggle_test_window:
            imgui.show_test_window()

        imgui.bullet_text("Input boxes are a little buggy:")
        imgui.indent()
        imgui.bullet()
        changed, text_val = imgui.input_text('label', text_val, 42)
        imgui.bullet_text("Right arrow key doesn't work")
        imgui.bullet_text("CMD+a or CTRL+a doesn't work")
        imgui.bullet_text("copy/pasting doesn't work (CMD+c, CMD+v)")
        imgui.unindent()
        imgui.bullet_text('Running pygame+IMgui uses about 15% CPU / 35MB memory')
        imgui.bullet_text('IMgui creates an imgui.ini file that holds state of windows')
        imgui.bullet_text('How do you make wrapping text?')
        imgui.bullet_text('Really good library. Default theme has great hacker aesthetic.')
        imgui.bullet_text("Can't change theme in python version: https://github.com/swistakm/pyimgui/issues/76")
        imgui.bullet_text("glfw/SDL/Cocos2d versions also work on my machine")
        imgui.indent()
        imgui.bullet_text("Cocos2d scrolling and animation is weird though -- scrolling changes frame rate :/")
        imgui.unindent()
        imgui.bullet_text("Rendering button with image inside:")
        imgui.indent()
        if imgui.image_button(image_texture, image_width, image_height):
            print('hi')
        imgui.unindent()

        imgui.bullet_text("Fonts, like images, are a little annoying to change:")
        imgui.push_font(alt_font)
        imgui.indent()
        imgui.bullet_text("This text should be in Arial 16px")
        imgui.unindent()
        imgui.pop_font()

        imgui.bullet_text("Is it possible to create a free-floating button not in a window? Don't think so")

        imgui.end()


        # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
        #       does not support fill() on OpenGL surfaces
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()

        pygame.display.flip()

if __name__ == "__main__":
    main()