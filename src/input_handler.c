// input_handler.c
#include <notcurses/notcurses.h>
#include <stdio.h>  // for fprintf
#include "input_handler.h"

int handle_input(struct ncinput* ni, int* selected, int option_count) {
  if (!ni || !selected || option_count <= 0) {
    fprintf(stderr, "[handle_input] invalid arguments\n");
    return -1;
  }

//support for tty
if (ni->evtype == NCTYPE_UNKNOWN) {
  fprintf(stderr, "[handle_input] unknown type — coercing to PRESS\n");
  ni->evtype = NCTYPE_PRESS;
}

switch (ni->evtype) {
	case NCTYPE_PRESS:
		switch (ni->id) {
        case 'q':
		return INPUT_QUIT;
	case NCKEY_UP:
		*selected = (*selected - 1 + option_count) % option_count;
          	return INPUT_NAVIGATE;

        case NCKEY_DOWN:
          	*selected = (*selected + 1) % option_count;
          	return INPUT_NAVIGATE;
	case NCKEY_ENTER:
		case '\n':
          		return INPUT_SELECT;
	default:
          	return INPUT_IGNORE;
		}

	default:
		fprintf(stderr, "[handle_input] ignored event type: %d\n", ni->evtype);
		return INPUT_IGNORE;
	}
}



