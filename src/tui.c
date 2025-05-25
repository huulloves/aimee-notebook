//v2 seperating input handling and main function
//tui2.c
//

#include <notcurses/notcurses.h>
#include <stdio.h>

// handles all input logic; returns when 'q' is pressed or error occurs
int input_handler(struct notcurses* nc) {
	struct ncinput ni;
	const uint32_t quit_key = 'q';

	while (1) {
		if (notcurses_get(nc, NULL, &ni) < 0) {
			return 1;
		}

	//log for input event, can comment out if not in use
	fprintf(stderr, "key id: %u, evtype: %d\n", ni.id, ni.evtype);

        if(ni.id == quit_key) {
		return 0;
	} else if(ni.id == 1115002) {
		fprintf(stderr, "\narrow up pressed\n");
		return 1;
	} else if(ni.id == 1115004) {
		fprintf(stderr, "\narrow down pressed\n");
		return 1;
	} else if(ni.id == 1115005) {
		fprintf(stderr, "\narrow left pressed\n");
		return 1;
	} else if(ni.id == 1115003) {
		fprintf(stderr, "\narrow right pressed\n");
		return 1;
	}
    }
}


//main function to call secondary functions
int main() {
	struct notcurses_options opts = {
		.termtype = NULL,
		.loglevel = NCLOGLEVEL_INFO,
		.flags = NCOPTION_INHIBIT_SETLOCALE
	};

	struct notcurses* nc = notcurses_init(&opts, NULL);
	if (!nc) return 1;

	struct ncplane* stdplane = notcurses_stdplane(nc);

	// stdplane holds background and title
	ncplane_putstr_yx(stdplane, 1, 2, "aimee says hello and welcome!");

	// create a box plane as a child (for options)
	int box_y = 3, box_x = 2;
	int box_rows = 9, box_cols = 40;
	
	struct ncplane_options box_opts = {
    		.y = box_y,
    		.x = box_x,
    		.rows = box_rows,
    		.cols = box_cols,
    		.userptr = NULL,
    		.name = "menu box",
   		.flags = NCPLANE_OPTION_HORALIGNED,
	};

	struct ncplane* box = ncplane_create(stdplane, &box_opts);
	if (!box) return 1;

	// draw box
	ncplane_perimeter_rounded(box, 0, 0, 0);

	// static message inside box
	ncplane_putstr_aligned(box, 5, NCALIGN_CENTER, "navigate using arrow keys");
	ncplane_putstr_aligned(box, 6, NCALIGN_CENTER, "or press q to quit");

	ncplane_putstr_yx(stdplane, 9, 1, "");

	notcurses_render(nc);

	int result = input_handler(nc);

	notcurses_stop(nc);
	return result;
}


