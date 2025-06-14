// input_handler.h shared module
#ifndef INPUT_HANDLER_H
#define INPUT_HANDLER_H

#include <notcurses/notcurses.h>

#define INPUT_IGNORE   0
#define INPUT_SELECT   1
#define INPUT_NAVIGATE 2
#define INPUT_QUIT    -1

int handle_input(struct ncinput* ni, int* selected, int option_count);

#endif // INPUT_HANDLER_H

