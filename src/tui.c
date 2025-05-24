// creates splash/landing page for tui program

#include <wchar.h>
#include <limits.h>
#include <string.h>
#include <notcurses/notcurses.h>

#include <notcurses/notcurses.h>

int main() {
    struct notcurses_options opts = {0};
    struct notcurses* nc = notcurses_init(&opts, NULL);
    if (!nc) return 1;

    struct ncplane* stdplane = notcurses_stdplane(nc);
    ncplane_putstr_yx(stdplane, 1, 1, "press 'q' to exit");
    notcurses_render(nc);

    struct ncinput ni;
    while (notcurses_get(nc, NULL, &ni) == 0 || ni.id != 'q');

    notcurses_stop(nc);
    return 0;
}


