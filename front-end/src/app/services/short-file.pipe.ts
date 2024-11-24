import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'shortFile'
})
export class ShortFilePipe implements PipeTransform {

  transform(value: string, maxLength: number): string {
    if (!value) return value;

    const extension = value.substring(value.lastIndexOf('.'));
    const nameWithoutExtension = value.substring(0, value.lastIndexOf('.'));

    if (nameWithoutExtension.length <= maxLength) {
      return value;
    }

    const truncatedName = nameWithoutExtension.substring(0, maxLength);
    return `${truncatedName}...${extension}`;
  }
}
