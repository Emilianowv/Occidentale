/* Read the actual keyboard keymap exported by a disposable Wayland compositor. */
#include <wayland-client.h>
#include <sys/mman.h>
#include <unistd.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static struct wl_keyboard *keyboard;
static const char *output;
static int done;

static void keymap(void *data, struct wl_keyboard *kb, uint32_t format, int32_t fd, uint32_t size) {
    (void)data; (void)kb;
    if (format != WL_KEYBOARD_KEYMAP_FORMAT_XKB_V1 || !size) exit(3);
    void *map = mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (map == MAP_FAILED) exit(4);
    FILE *f = fopen(output, "wb");
    if (!f) exit(5);
    if (fwrite(map, 1, size-1, f) != size-1) exit(6);
    fclose(f);
    munmap(map, size);
    close(fd);
    done = 1;
}
static void enter(void *d, struct wl_keyboard *k, uint32_t s, struct wl_surface *w, struct wl_array *a) {(void)d;(void)k;(void)s;(void)w;(void)a;}
static void leave(void *d, struct wl_keyboard *k, uint32_t s, struct wl_surface *w) {(void)d;(void)k;(void)s;(void)w;}
static void key(void *d, struct wl_keyboard *k, uint32_t s, uint32_t t, uint32_t c, uint32_t v) {(void)d;(void)k;(void)s;(void)t;(void)c;(void)v;}
static void modifiers(void *d, struct wl_keyboard *k, uint32_t s, uint32_t a, uint32_t b, uint32_t c, uint32_t g) {(void)d;(void)k;(void)s;(void)a;(void)b;(void)c;(void)g;}
static void repeat(void *d, struct wl_keyboard *k, int32_t r, int32_t l) {(void)d;(void)k;(void)r;(void)l;}
static const struct wl_keyboard_listener keyboard_listener = {keymap, enter, leave, key, modifiers, repeat};
static void capabilities(void *data, struct wl_seat *seat, uint32_t caps) {
    (void)data;
    if ((caps & WL_SEAT_CAPABILITY_KEYBOARD) && !keyboard) {
        keyboard = wl_seat_get_keyboard(seat);
        wl_keyboard_add_listener(keyboard, &keyboard_listener, NULL);
    }
}
static void seat_name(void *d, struct wl_seat *s, const char *n) {(void)d;(void)s;(void)n;}
static const struct wl_seat_listener seat_listener = {capabilities, seat_name};
static void global(void *data, struct wl_registry *registry, uint32_t name, const char *interface, uint32_t version) {
    (void)data;
    if (!strcmp(interface, wl_seat_interface.name)) {
        struct wl_seat *seat = wl_registry_bind(registry, name, &wl_seat_interface, version < 7 ? version : 7);
        wl_seat_add_listener(seat, &seat_listener, NULL);
    }
}
static void removed(void *d, struct wl_registry *r, uint32_t n) {(void)d;(void)r;(void)n;}
static const struct wl_registry_listener registry_listener = {global, removed};
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    output = argv[1];
    struct wl_display *display = wl_display_connect(NULL);
    if (!display) return 7;
    struct wl_registry *registry = wl_display_get_registry(display);
    wl_registry_add_listener(registry, &registry_listener, NULL);
    for (int i=0; !done && i<100; i++) {
        if (wl_display_roundtrip(display) < 0) return 8;
        if (!done) usleep(50000);
    }
    wl_display_disconnect(display);
    return done ? 0 : 9;
}
