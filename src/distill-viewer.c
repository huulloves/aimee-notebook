//v1.0 distill-viewer.c
// based on start.c, simplified for static "distill view"

#include <notcurses/notcurses.h>
#include <stdio.h>

struct ncplane* setup_viewbox(struct notcurses* nc) {
	struct ncplane* stdplane = notcurses_stdplane(nc);
	ncplane_erase(stdplane);
	ncplane_putstr_yx(stdplane, 1, 2, "aimee distills...");

	// get terminal dimensions
	int term_rows, term_cols;
	ncplane_dim_yx(stdplane, &term_rows, &term_cols);

	struct ncplane_options box_opts = {
		.y = 2,
		.x = 2,
		.rows = term_rows - 4,
		.cols = term_cols - 4,
		.userptr = NULL,
		.name = "viewbox",
		.flags = NCPLANE_OPTION_HORALIGNED,
	};

	struct ncplane* box = ncplane_create(stdplane, &box_opts);
	if (!box) return NULL;

	ncplane_erase(box);
	ncplane_perimeter_rounded(box, 0, 0, 0);

	ncplane_set_styles(box, NCSTYLE_ITALIC);
	ncplane_putstr_aligned(box, 2, NCALIGN_CENTER, "this is your distill view");
	ncplane_putstr_aligned(box, 4, NCALIGN_CENTER, "press q to exit");

	return box;
}

int main() {
	struct notcurses_options opts = {
		.termtype = NULL,
		.loglevel = NCLOGLEVEL_INFO,
		.flags = NCOPTION_SUPPRESS_BANNERS,
	};

	struct notcurses* nc = notcurses_init(&opts, NULL);
	if (!nc) return 1;

	struct ncplane* box = setup_viewbox(nc);
	if (!box) return 1;

	notcurses_render(nc);

	struct ncinput ni;
	while (1) {
		if (notcurses_get(nc, NULL, &ni) < 0) break;
		if (ni.id == 'q') break;
	}

	ncplane_destroy(box);
	notcurses_stop(nc);
	return 0;
}

