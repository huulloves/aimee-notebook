//v1.3 adding event-driven static menu box 
// + input_handler module
//start.c
//

#include <notcurses/notcurses.h>
#include <stdio.h>
#include "input_handler.h"

#define OPTION_COUNT 3

const char* menu_options[OPTION_COUNT] = {"speak", "distill", "exit"};

// draws the menu in-place on an existing box plane
void draw_menu_box(struct ncplane* box, int selected) {
	ncplane_erase(box);
	ncplane_perimeter_rounded(box, 0, 0, 0);

	for (int i = 0; i < OPTION_COUNT; ++i) {
		if (i == selected) {
			ncplane_set_styles(box, NCSTYLE_BOLD | NCSTYLE_UNDERLINE);
		} else {
			ncplane_set_styles(box, NCSTYLE_NONE);
		}
		ncplane_putstr_aligned(box, 2 + i, NCALIGN_CENTER, menu_options[i]);
	}

	ncplane_set_styles(box, NCSTYLE_ITALIC);
	ncplane_putstr_aligned(box, 6, NCALIGN_CENTER, "navigate with arrow keys");
	ncplane_putstr_aligned(box, 7, NCALIGN_CENTER, "press enter to select | q to quit");
}

// sets up the static splash screen layout
struct ncplane* setup_menu_plane(struct notcurses* nc) {
	struct ncplane* stdplane = notcurses_stdplane(nc);
	ncplane_erase(stdplane);
	ncplane_putstr_yx(stdplane, 1, 2, "aimee says hello and welcome!");

	struct ncplane_options box_opts = {
		.y = 3,
		.x = 2,
		.rows = 9,
		.cols = 40,
		.userptr = NULL,
		.name = "menu box",
		.flags = NCPLANE_OPTION_HORALIGNED,
	};

	struct ncplane* box = ncplane_create(stdplane, &box_opts);
	return box;
}

int main() {
	struct notcurses_options opts = {
		.termtype = NULL,
		.loglevel = NCLOGLEVEL_INFO,
		//.flags = NCOPTION_INHIBIT_SETLOCALE
	};

	struct notcurses* nc = notcurses_init(&opts, NULL);
	if (!nc) return 1;

	int selected = 0;
	struct ncinput ni;
	int result;
	struct ncplane* box = setup_menu_plane(nc);
	if (!box) return -1;
	draw_menu_box(box, selected);
	notcurses_render(nc);

	while (1) {
		if (notcurses_get(nc, NULL, &ni) < 0) break;
		result = handle_input(&ni, &selected, OPTION_COUNT);

		if (result == -1) {
			ncplane_destroy(box);
			break;
		} else if (result == 1) {
			ncplane_destroy(box);
			break;
		} else {
			draw_menu_box(box, selected);
			notcurses_render(nc);
		}
	}

	notcurses_stop(nc);

	if (result == 1) {
		printf("you selected: %s\n", menu_options[selected]);
	}

	return 0;
}



