import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

/**
 * An example element.
 *
 * @slot - This element has a slot
 * @csspart button - The button
 */
@customElement('cwv-bar-graph')
export class CWVBarGraph extends LitElement {
  @property() value: number = 0;

  static styles = css`
    :host {
      --_cwv-percent-bg: var(--cwv-percent-bg, #e6e6e6);
      display: block;
    }

    .bar {
      display: block;
      background: none;
    }
  `;

  protected updated(changed: any): void {
    if (changed.has('value') && !!this.value) {
      const cleanValue = Math.min(this.value, 100);

      // Set the linear gradient as the background
      const style = this.calculateBarGraph(cleanValue);
      if (style) {
        this.style.setProperty('background', style);
      }
    }
  }

  calculateBarGraph(value: number): string | undefined {
    if (value <= 0) {
      return;
    }

    return `linear-gradient(90deg, var(--_cwv-percent-bg) 0%, var(--_cwv-percent-bg) ${value}%, transparent ${value}%)`;
  }

  render() {
    return html`
      <span class="bar">
        <slot></slot>
      </span>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'cwv-bar-graph': CWVBarGraph;
  }
}
