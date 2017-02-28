import numpy
import h5py
from itertools import product

class H5PYDataset:
    @staticmethod
    def create_split_array(split_dict):
        """Create a valid array for the `split` attribute of the root node.

        Parameters
        ----------
        split_dict : dict
            Maps split names to dict. Those dict map source names to
            tuples. Those tuples contain two, three or four elements:
            the start index, the stop index, (optionally) subset
            indices and (optionally) a comment.  If a particular
            split/source combination isn't present in the split dict,
            it's considered as unavailable and the `available` element
            will be set to `False` it its split array entry.

        """
        # Determine maximum split, source and string lengths
        split_len = max(len(split) for split in split_dict)
        sources = set()
        comment_len = 1
        for split in split_dict.values():
            sources |= set(split.keys())
            for val in split.values():
                if len(val) == 4:
                    comment_len = max([comment_len, len(val[-1])])
        sources = sorted(list(sources))
        source_len = max(len(source) for source in sources)

        # Instantiate empty split array
        split_array = numpy.empty(
            len(split_dict) * len(sources),
            dtype=numpy.dtype([
                ('split', 'a', split_len),
                ('source', 'a', source_len),
                ('start', numpy.int64, 1),
                ('stop', numpy.int64, 1),
                ('indices', h5py.special_dtype(ref=h5py.Reference)),
                ('available', numpy.bool, 1),
                ('comment', 'a', comment_len)]))

        # Fill split array
        for i, (split, source) in enumerate(product(split_dict, sources)):
            if source in split_dict[split]:
                start, stop = split_dict[split][source][:2]
                available = True
                indices = h5py.Reference()
                # Workaround for bug when pickling an empty string
                comment = '.'
                if len(split_dict[split][source]) > 2:
                    indices = split_dict[split][source][2]
                if len(split_dict[split][source]) > 3:
                    comment = split_dict[split][source][3]
                    if not comment:
                        comment = '.'
            else:
                (start, stop, indices, available, comment) = (
                    0, 0, h5py.Reference(), False, '.')
            # Workaround for H5PY being unable to store unicode type
            split_array[i]['split'] = split.encode('utf8')
            split_array[i]['source'] = source.encode('utf8')
            split_array[i]['start'] = start
            split_array[i]['stop'] = stop
            split_array[i]['indices'] = indices
            split_array[i]['available'] = available
            split_array[i]['comment'] = comment.encode('utf8')

        return split_array