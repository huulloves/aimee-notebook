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

        if(ni.evtype == NCTYPE_PRESS) {
		if(ni.id == quit_key) {
			return 0;
		} else if(ni.id == NCKEY_UP) {
			fprintf(stderr, "arrow up pressed\n");
		} else if(ni.id == NCKEY_DOWN) {
			fprintf(stderr, "arrow down pressed\n");
		} else if(ni.id == NCKEY_LEFT) {
			fprintf(stderr, "arrow left pressed\n");
		} else if(ni.id == NCKEY_RIGHT) {
			fprintf(stderr, "arrow right pressed\n");
		}
	}
    }
}

int main() {
	struct notcurses_options opts = {
		.termtype = NULL,
		.loglevel = NCLOGLEVEL_INFO,
		.flags = NCOPTION_INHIBIT_SETLOCALE
	};

	struct notcurses* nc = notcurses_init(&opts, NULL);
	if (!nc) return 1;

	struct ncplane* stdplane = notcurses_stdplane(nc);
	ncplane_putstr_yx(stdplane, 1, 1, "press 'q' to exit");
	notcurses_render(nc);

	int result = input_handler(nc);

	notcurses_stop(nc);

	return result;
}

